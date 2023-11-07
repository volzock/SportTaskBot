class Docmaster:
    __docs = None

    def __init__(self):
        self.__docs = []

    def docs(self, name, description, role):
        self.__docs.append({"name": name, "description": description, "role": role})

        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def print_user_funcs(self):
        res = ""
        for row in self.__docs:
            if row["role"] == "user":
                res += "<b>" + row["name"] + "</b>"
                res += ' - '
                res += row["description"]
                res += '\n'
        return res

    def print_admin_funcs(self):
        res = ""
        for row in self.__docs:
            res += "<b>" + row["name"] + "</b>"
            res += ' - '
            res += row["description"]
            res += '\n'
        return res
