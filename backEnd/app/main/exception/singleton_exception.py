class SingletonException(Exception):
    def __init__(
        self, message="Singleton classes cannot be instantiated by contructor. Consider using getInstance method."
    ):
        self.message = message
        super().__init__(self.message)