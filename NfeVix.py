from RPA import *
import calendar
import datetime

class NfeVix:

    rpa = None
    site = "https://nfse.vitoria.es.gov.br"

    def __init__(self, driver, login, senha, ins):

        # RPA
        self.rpa = RPA(driver)

        # abre o site
        self.rpa.open(self.site)

        # entrar com login e senha
        self.rpa.elem("input[id='login']").input(login)
        self.rpa.elem("input[id='senha']").input(senha)
        self.rpa.elem("input[value='Acessar']").click()

        # selecionar empresa
        self.rpa.elem("tr[data-ins='{}']".format(ins)).click()

    def baixar(self, mes):

        # operar lotes
        self.rpa.elem("a[href='formLote.cfm']").click()

        # buscar notas
        ano = datetime.date.today().year
        _, dia = calendar.monthrange(ano, mes)
        dia = "0{}".format(dia) if dia < 10 else str(dia)
        mes = "0{}".format(mes) if mes < 10 else str(mes)
        self.rpa.elem("input[name='inicioC']").input("01{}{}".format(mes, ano))
        self.rpa.elem("input[name='fimC']").input("{}{}{}".format(dia, mes, ano))
        self.rpa.script("buscarNotas()")

        # selecionar "baixar"
        self.rpa.elem("input[value='B']").click()
        self.rpa.script("operarLote()")

        return self.rpa.file()

    def fechar(self):

        # fecha o navegador
        self.rpa.close()