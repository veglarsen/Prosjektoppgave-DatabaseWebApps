class Blogg:

    # construct / attributes
    def __init__(self, blogg_navn, blogg_ID, eier):
        self.blogg_navn = blogg_navn
        self.blogg_ID = blogg_ID
        self.eier = eier


class Innlegg:

    # construct / attributes
    def __init__(self, blogg_navn, innlegg_ID, blogg_ID, innlegg, dato, treff, ingress, tittel, eier):
        self.blogg_navn = blogg_navn
        self.innlegg_ID = innlegg_ID
        self.blogg_ID = blogg_ID
        self.innlegg = innlegg
        self.dato = dato
        self.treff = treff
        self.ingress = ingress
        self.tittel = tittel
        self.eier = eier


class InnleggTag:

    # construct / attributes
    def __init__(self, blogg_navn, innlegg_ID, blogg_ID, innlegg, dato, treff, ingress, tittel, eier, tag_navn):
        self.blogg_navn = blogg_navn
        self.innlegg_ID = innlegg_ID
        self.blogg_ID = blogg_ID
        self.innlegg = innlegg
        self.dato = dato
        self.treff = treff
        self.ingress = ingress
        self.tittel = tittel
        self.eier = eier
        self.tag_navn = tag_navn


class Kommentar:

    # construct / attributes
    def __init__(self, kommentar_ID, innlegg_ID, blogg_ID, bruker, kommentar, dato):
        self.kommentar_ID = kommentar_ID
        self.innlegg_ID = innlegg_ID
        self.blogg_ID = blogg_ID
        self.bruker = bruker
        self.kommentar = kommentar
        self.dato = dato


class Vedlegg:

    # construct / attributes
    def __init__(self, vedlegg_ID, fil_navn, fil_type, fil_data, size, innlegg_ID):
        self.vedlegg_ID = vedlegg_ID
        self.fil_navn = fil_navn
        self.fil_type = fil_type
        self.fil_data = fil_data
        self.size = size
        self.innlegg_ID = innlegg_ID


# class Bruker():
#
#     # construct / attributes
#     def __init__(self, bruker, etternavn, fornavn, passord, eMail):
#         self.bruker = bruker
#         self.etternavn = etternavn
#         self.fornavn = fornavn
#         self.passord = passord
#         self.eMail = eMail
#         self.is_authenticated = False
#         self.is_active = True
#         self.is_anonymous = False

class Tag():

    # construct / attributes
    def __init__(self, tag_ID, tag_navn, ):
        self.tag_ID = tag_ID
        self.tag_navn = tag_navn
