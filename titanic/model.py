"""
['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp',
      'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
PassengerId 고객아이디
Survived 생존여부     Survival    0 = No, 1 = Yes
Pclass 승선권 클래스    Ticket class    1 = 1st, 2 = 2nd, 3 = 3rd
Name 이름
Sex  성별  Sex
Age  나이  Age in years
SibSp  동반한 형제자매, 배우자 수  # of siblings / spouses aboard the Titanic
Parch  동반한 부모, 자식 수  # of parents / children aboard the Titanic
Ticket  티켓 번호  Ticket number
Fare  티켓의 요금  Passenger fare
Cabin  객실번호  Cabin number
Embarked  승선한 항구명  Port of Embarkation
 C = Cherbourg 쉐부로, Q = Queenstown 퀸스타운, S = Southampton 사우스햄톤
"""
import pandas as pd
import numpy as np

class TitanicModel:
    def __init__(self):
        self._context = None
        self._fname = None
        self._train = None
        self._test = None
        self._test_id = None

    @property
    def context(self) -> object:return self._context

    @context.setter
    def context(self, context): self._context = context

    @property
    def fname(self) -> object: return self._fname

    @fname.setter
    def fname(self, fname): self._fname = fname

    @property
    def train(self) -> object: return self._train

    @train.setter
    def train(self, train): self._train = train

    @property
    def test(self)-> object: return self._test

    @test.setter
    def test(self, test): self._test = test

    @property
    def test_id(self)-> object: return self._test_id

    @test_id.setter
    def test_id(self, test_id): self._test_id = test_id

    def new_file(self) -> str: return self._context + self._fname

    def new_dframe(self) -> object:
        file = self.new_file()
        return pd.read_csv(file)

    def hook_process(self, train, test) -> object:
        print('-------------1. Cabin, Ticket 삭제 ---------------')
        t = self.drop_feature(train, test, 'Cabin')
        t = self.drop_feature(t[0], t[1], 'Ticket')
        print('-------------2. Embarked 편집 --------------------')
        t = self.embarked_norminal(t[0], t[1])
        print('-------------3. Title 편집 -----------------------')
        t = self.title_nominal(t[0], t[1])
        print('-------------4. Name, PassengerId 삭제------------')
        t = self.drop_feature(t[0], t[1], 'Name')
        #
        t = self.drop_feature(t[0], t[1], 'PassengerId')
        print('-------------5. Age 편집------------')
        t = self.age_ordinal(t[0], t[1])
        print('-------------6. Age 삭제------------')
        t = self.drop_feature(t[0], t[1], 'Age')
        print('-------------7. Fare 편집------------')
        t = self.fare_ordinal(t[0], t[1])
        print('-------------8. Fare 삭제------------')
        t = self.drop_feature(t[0], t[1], 'Fare')
        print('-------------9. Sex 편집 ---------------------------------')
        t = self.sex_nominal(t[0], t[1])
        t[1] = t[1].fillna({"FareBand" : 1})
        a = self.null_sum(t[1])
        print('널의 수량 {} 개'.format(a))
        self._test = t[1]
        return t[0]

    @staticmethod
    def null_sum(train)->int:
        sum = train.isnull().sum()
        return sum

    @staticmethod
    def drop_feature(train,test,feature)->[]:
        train = train.drop([feature], axis = 1)
        test = test.drop([feature], axis=1)
        # print(train.head())
        # print(train.columns)
        return [train, test]

    @staticmethod
    def embarked_norminal(train, test)->[]:
        s_city = train[train['Embarked'] =='S'].shape[0]  # 스칼라
        c_city = train[train['Embarked'] =='C'].shape[0]  # 스칼라
        q_city = train[train['Embarked'] =='Q'].shape[0]  # 스칼라

        # print("S 에서 승선한 탑승객 수: {}".format(s_city))
        # print("C 에서 승선한 탑승객 수: {}".format(c_city))
        # print("Q 에서 승선한 탑승객 수: {}".format(q_city))

        train = train.fillna({"Embarked":"S"})
        city_mapping = {"S" : 1, "C" : 2, "Q" : 3}
        train['Embarked'] = train['Embarked'].map(city_mapping)
        test['Embarked'] = test['Embarked'].map(city_mapping)
        # print(train.head())
        # print(train.columns)
        return [train, test]

    @staticmethod
    def title_nominal(train, test)->[]:
        combine = [train, test]
        for dataset in combine:
            dataset['Title'] = dataset.Name.str.extract('([A-Za-z]+)\.', expand=False)

        for dataset in combine:
            dataset['Title'] \
                = dataset['Title'].replace(['Capt', 'Col','Don', 'Dr', 'Major', 'Rev', 'Jonkheer', 'Dona'], 'Rare')
            dataset['Title'] \
                = dataset['Title'].replace(['Countess', 'Lady', 'Sir'], 'Royal')
            dataset['Title'] \
                = dataset['Title'].replace(['Mlle', 'Ms'], 'Miss')
            dataset['Title'] \
                = dataset['Title'].replace('Mne', 'Mrs')
        train[['Title','Survived']].groupby(['Title'], as_index=False).mean()
        # print(train[['Title','Survived']].groupby(['Title'], as_index=False).mean())
        """
            Title  Survived
        0  Master  0.575000
        1    Miss  0.702703
        2     Mme  1.000000
        3      Mr  0.156673
        4     Mrs  0.792000
        5    Rare  0.250000
        6   Royal  1.000000
        """

        title_mapping = {'Mr':1, 'Miss':2, 'Mrs':3, 'Master':4,'Royal':5, 'Rare':6, 'Mme':7 }

        for dataset in combine:
            dataset['Title'] = dataset['Title'].map(title_mapping)
            dataset['Title'] = dataset['Title'].fillna(0)
        return [train, test]

    @staticmethod
    def sex_nominal(train, test)->[]:
        combine = [train,test]
        sex_mapping = {'male':0, 'female':1}
        for dataset in combine:
            dataset['Sex'] = dataset['Sex'].map(sex_mapping)

        return [train, test]


    @staticmethod
    def age_ordinal(train, test) ->[]:
        train['Age'] = train['Age'].fillna(-0.5)
        test['Age'] = test['Age'].fillna(-0.5)
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf ]
        labels = ['Unknown','Baby','Child','Teenager','Student','Young Adult', 'Adult', 'Senior']
        train['AgeGroup'] = pd.cut(train['Age'], bins, labels = labels)
        test['AgeGroup'] = pd.cut(test['Age'], bins, labels=labels)

        age_title_mapping = {0: 'Unknown', 1 : 'Baby', 2: 'Child', 3: 'Teenager', 4 : 'Student',
                             5 : 'Young Adult', 6: 'Adult', 7: 'Senior'}
        for x in range(len(train['AgeGroup'])):
            if train['AgeGroup'][x] == 'Unknown':
                train['AgeGroup'][x] = age_title_mapping[train['Title'][x]]

        for x in range(len(test['AgeGroup'])):
            if test['AgeGroup'][x] == 'Unknown':
                test['AgeGroup'][x] = age_title_mapping[test['Title'][x]]

        age_mapping = {'Baby': 1, 'Child' :2, 'Teenager':3, 'Student':4,'Young Adult':5, 'Adult':6, 'Senior':7 }
        train['AgeGroup'] = train['AgeGroup'].map(age_mapping)
        test['AgeGroup'] = test['AgeGroup'].map(age_mapping)
        print(train['AgeGroup'].head())

        return [train, test]


    @staticmethod
    def fare_ordinal(train, test)->[]:
        train['FareBand'] = pd.qcut(train['Fare'], 4, labels={1, 2, 3, 4})
        test['FareBand'] = pd.qcut(test['Fare'], 4, labels={1, 2, 3, 4})
        return [train,test]





