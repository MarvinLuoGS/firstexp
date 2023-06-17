from otree.api import *


doc = """
Examples for group matching
"""


class C(BaseConstants):
    NAME_IN_URL = 'group_matching'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 5
    PRINCIPAL_ROLE = 'principal'
    AGENT_ROLE = 'agent'
    R_NUM = 2


class Subsession(BaseSubsession):
    role_list = models.StringField()


def creating_session(subsession):
    import random
    #无论哪种方式，总体的思路都是搞出一个group_matrix让后传给set_group_matrix
    #这样可以利用内置的group、id_in_group和role属性以及他们的相应方法
    ##固定角色+每轮固定搭配（什么都不设置即为默认的分组方法，内置的方法所有轮次P1肯定和P2匹配，P3肯定和P4匹配，id_in_group是按1212的顺序分配）
    print(subsession.get_group_matrix())
    #固定角色和固定搭配的情况下，只需要在第一轮做好随机分配即可，后续轮次复制第一轮的结果即可，与内置方法的差异是P1不一定和P2匹配了
    if subsession.round_number == 1:
        num_participant = len(subsession.get_players()) #获得实际的参加人数，get_players返回的是一个列表
        participant_list = [ x for x in range(1,num_participant+1)] #生成一个[1,2,3,4,5,6]这样的列表，这个列表将用于后续的矩阵生成
        random.shuffle(participant_list) #随机步骤，将列表打乱
        group_matrix = [] #生成一个空的列表，往其中添加元素生成矩阵
        for i in range(1,int(num_participant/C.PLAYERS_PER_GROUP) + 1): #要分几个组，就往其中填入几个空列表作为元素
            group_matrix.append([])
            i += 1
        i = 0
        for li in group_matrix: #对group_matrix里面的每个空列表进行循环，往其中依次填入数字
            while len(li) < C.PLAYERS_PER_GROUP: #在空列表中的元素个数没达到小组人数时依次往里面填入数字，达到小组人数时停止填入，继续往下一个列表填入
                li.append(participant_list[i])
                i += 1
        subsession.set_group_matrix(group_matrix) #所有的空列表都填充完成，分组矩阵已生成，使用set_group_matrix进行分组
    else:
        subsession.group_like_round(1) #通过group_like_round()复制第一轮的分组结果
    print(subsession.get_group_matrix()) #输出所有轮次分组匹配的结果matrix，可以看到所有轮次中的matrix都是一样的
    #无固定角色+每轮随机匹配，实际上就是所有被试都是相同角色然后进行随机匹配和上面的区别就是后续的轮次不用复制第一轮的结果，每轮都是重新随机
    num_participant = len(subsession.get_players())
    participant_list = [ x for x in range(1,num_participant+1)]
    random.shuffle(participant_list)
    group_matrix = []
    for i in range(1,int(num_participant/C.PLAYERS_PER_GROUP) + 1):
        group_matrix.append([])
        i += 1
    i = 0
    for li in group_matrix:
        while len(li) < C.PLAYERS_PER_GROUP:
            li.append(participant_list[i])
            i += 1
    subsession.set_group_matrix(group_matrix)
    print(subsession.get_group_matrix())
    #无固定角色+每轮随机匹配（内置方法和自己写的无差异）
    subsession.group_randomly()
    print(subsession.get_group_matrix())
    #有固定角色+每轮随机匹配，分配的重点在于随机分配角色，并将不同角色之间进行匹配，和内置方法相比不再按顺序分配id_in_group
    num_participant = len(subsession.get_players()) #获得实际的参加人数，get_players返回的是一个列表
    if subsession.round_number == 1: #这里的第一轮要随机生成的一个列表只是角色编号的列表，比如[2,1,1,2,1,2]
        role_list = [x for x in range(1,C.R_NUM+1)] * int(num_participant/C.PLAYERS_PER_GROUP) #将[1,2]这样的列表按组数扩展
        random.shuffle(role_list) #将角色列表随机排列
        subsession.role_list = str(role_list) #将随机后的角色列表以字符型格式保存（为什么这样保存？）
    else:
        prev_subsession = subsession.in_round(1) #后续的轮次找到第1轮的subsession对象（为什么是对象？）
        subsession.role_list = prev_subsession.role_list #将第1轮的subsession对象的role_list字段复制过来，就获得了角色分配列表
    ####由于拿来的是字符串，带有括号和空格等字符，所以需要去除不必要的字符、拼合为列表、将列表的字符型的数字转换为数值型
    role_list = subsession.role_list.strip("[")
    role_list = role_list.strip("]")
    role_list = role_list.replace(" ","")
    role_list = role_list.split(",")
    role_list = list(map(eval,role_list))
    ##########
    ##已经获得角色分配列表后，下一步是按角色进行匹配，思路是将被试按角色分为两个pool，每次匹配分别从两个pool拿出一个进行匹配
    role_list_temp = [x for x in range(1,C.R_NUM+1)] #作为分组对照的列表[1,2]
    role_matrix = [] #将角色分为两个pool，包含两个pool的矩阵
    for i in range(1,C.R_NUM+1): #按角色数量先生成对应数量的空列表
        role_matrix.append([])
        i += 1
    ##先分配好第一个角色pool，再分配第二个角色pool，另一种实现方法是将这个时候获得的role_matrix储存起来，同样需要考虑如何将字符串转化为列表
    for j in range(0,C.R_NUM):
        for i in range(0,num_participant):
            if role_list[i] == role_list_temp[j]:
                role_matrix[j].append(i+1)
        j += 1
    ##每个pool里面进行随机
    for j in range(0,C.R_NUM):
        random.shuffle(role_matrix[j])
        j += 1
    ##用于分组的matrix
    group_matrix = []
    for i in range(1,int(num_participant/C.PLAYERS_PER_GROUP) + 1):
        group_matrix.append([])
        i += 1
    ##按角色往分组matrix里面放入编号
    i = 0
    while i < int(num_participant/C.PLAYERS_PER_GROUP): #i表示组别
        for j in range(0,C.R_NUM): #j表示角色编号
            group_matrix[i].append(role_matrix[j][i]) #先往i组里放入角色j，再放入角色j+1
            j += 1 
        i += 1 #i组中已放入j、j+1角色，i组的分配已完成，分配i+1组，直到分配完所有组
    subsession.set_group_matrix(group_matrix) #当轮分组矩阵已生成，使用set_group_matrix进行分组
    print(subsession.get_group_matrix())
    #有固定角色+每轮随机匹配(内置方法)，内置方法的分配会按顺序分配id_in_group即角色，比如P1是1，P2是2，P3是1，P4是2
    subsession.group_randomly(fixed_id_in_group=True)
    print(subsession.get_group_matrix())


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    pass


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
