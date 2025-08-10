import abc

class Repository(metaclass = abc.ABCMeta):

    @abc.abstractmethod
    def store_puzzle(self):
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_stored_puzzle(self, print_date):
        raise NotImplementedError

    @abc.abstractmethod
    def store_solution(self):
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_stored_solution(self):
        raise NotImplementedError

    @abc.abstractmethod
    def retrieve_embeddings(self, words : list):
        raise NotImplementedError

