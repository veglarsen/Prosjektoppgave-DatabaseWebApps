class Blogg:

    # construct / attributes
    def __init__(self, blogg_navn):
        self.blogg_navn = blogg_navn

class Innlegg:

    # construct / attributes
    def __init__(self, innlegg_id, blogg_ID, innlegg, dato, tag, treff):
        self.innlegg_id = innlegg_id
        self.blogg_ID = blogg_ID
        self.innlegg = innlegg
        self.dato = dato
        self.tag = tag
        self.treff = treff

class Kommentar:

    # construct / attributes
    def __init__(self, kommentar_ID, innlegg_ID, blogg_ID, bruker, kommentar, dato):
        self.kommentar_ID = kommentar_ID
        self.innlegg_ID =  innlegg_ID
        self.blogg_ID = blogg_ID
        self.bruker = bruker
        self.kommentar = kommentar
        self.dato = dato
