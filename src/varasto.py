class Varasto:
    def __init__(self, tilavuus, alku_saldo=0):
        self.tilavuus = tilavuus
        self.saldo = alku_saldo

    def paljonko_mahtuu(self):
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        self.saldo = self.saldo + maara

    def ota_varastosta(self, maara):
        self.saldo = self.saldo - maara
        return maara
