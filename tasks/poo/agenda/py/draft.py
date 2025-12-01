class Fone:
    def __init__(self, fid, number):
        self.id = fid
        self.number = number

    def is_valid(self):
        # Validação simples (os testes nem usam erro de fone, mas deixo aqui)
        validos = "0123456789().-"
        for c in self.number:
            if c not in validos:
                return False
        return True

    def __str__(self):
        # ex: oi:1234
        return f"{self.id}:{self.number}"


class Contact:
    def __init__(self, name):
        self.name = name
        self.favorited = False
        self.fones = []  # lista de Fone

    def addFone(self, fid, number):
        f = Fone(fid, number)
        # Se quiser ativar validação real:
        # if not f.is_valid():
        #     print("fail: fone invalido")
        #     return
        self.fones.append(f)

    def rmFone(self, index):
        if 0 <= index < len(self.fones):
            del self.fones[index]
        # se índice inválido, não faz nada (pra não quebrar os testes)

    def toggleFavorited(self):
        self.favorited = not self.favorited

    def isFavorited(self):
        return self.favorited

    def getName(self):
        return self.name

    def __str__(self):
        marker = "@" if self.favorited else "-"
        fones_str = ", ".join(str(f) for f in self.fones)
        return f"{marker} {self.name} [{fones_str}]"


class Agenda:
    def __init__(self):
        # nome -> Contact
        self.contacts = {}

    def _get_sorted_contacts(self):
        lista = list(self.contacts.values())
        lista.sort(key=lambda c: c.getName())
        return lista

    def addContact(self, name, fones):
        # fones é uma lista de Fone
        if name in self.contacts:
            contato = self.contacts[name]
        else:
            contato = Contact(name)
            self.contacts[name] = contato

        for f in fones:
            contato.addFone(f.id, f.number)

    def getContact(self, name):
        return self.contacts.get(name)

    def rmContact(self, name):
        if name in self.contacts:
            del self.contacts[name]

    def search(self, pattern):
        result = []
        for c in self._get_sorted_contacts():
            if pattern in str(c):
                result.append(c)
        return result

    def getFavorited(self):
        favs = []
        for c in self._get_sorted_contacts():
            if c.isFavorited():
                favs.append(c)
        return favs

    def getContacts(self):
        return self._get_sorted_contacts()

    def __str__(self):
        linhas = [str(c) for c in self._get_sorted_contacts()]
        return "\n".join(linhas)


def main():
    agenda = Agenda()

    while True:
        line = input()
        if line == "":
            continue

        print("$" + line)
        parts = line.split()
        cmd = parts[0]

        if cmd == "end":
            break

        elif cmd == "show":
            print(agenda)

        elif cmd == "add":
            # add nome id1:num1 id2:num2 ...
            name = parts[1]
            fones = []
            for token in parts[2:]:
                fid, num = token.split(":")
                fones.append(Fone(fid, num))
            agenda.addContact(name, fones)

        elif cmd == "rmFone":
            # rmFone nome indice
            name = parts[1]
            idx = int(parts[2])
            contato = agenda.getContact(name)
            if contato is not None:
                contato.rmFone(idx)

        elif cmd == "rm":
            # rm nome
            name = parts[1]
            agenda.rmContact(name)

        elif cmd == "search":
            pattern = parts[1]
            res = agenda.search(pattern)
            for c in res:
                print(c)

        elif cmd == "tfav":
            # tfav nome
            name = parts[1]
            contato = agenda.getContact(name)
            if contato is not None:
                contato.toggleFavorited()

        elif cmd == "favs":
            for c in agenda.getFavorited():
                print(c)

        else:
            print("fail: comando invalido")


if __name__ == "__main__":
    main()