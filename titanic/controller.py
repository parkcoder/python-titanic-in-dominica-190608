from titanic.model import TitanicModel

class TitanicController:
    def __init__(self):
        self._m = TitanicModel()
        self._context = './data/'
        self._train = self.create_train()

    def create_train(self) -> object:
        m = self._m
        m.context = self._context
        m.fname = 'train.csv'
        t1 = m.new_dframe()
        print('---------- train head & column -----------')
        print(t1.head())

        m.fname = 'test.csv'
        t2 = m.new_dframe()
        print('---------- test head & column -----------')
        print(t2.head())

        print('---------- hook 메소드 시작 -----------')
        # train = m.hook_process(t1, t2)
        print('---------- 1 -----------')
        # print(train.column)
        print('---------- 2 -----------')
        # print(train.head())
        # return train

    def create_model(self):
        pass