class SingletonException(Exception):
    def __init__(self):
        self.message = (
            message
        ) = "Singleton classes cannot be instantiated by contructor. Consider using getInstance method."
        super().__init__(self.message)