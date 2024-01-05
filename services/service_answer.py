class ServiceAnswer:
    success: bool
    first_wa: int

    def __str__(self) -> str:
        if self.success:
            return "✅ Поздравляю, прошло проверку, молодец!"
        return f"❌ Ничего, Москва не за один день строилась, первый непройденный тест: {self.first_wa}"
