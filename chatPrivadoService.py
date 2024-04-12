class ChatPrivadoService:
    def __init__(self):
        self.misatges_list = []

    def enviarmisatge(self, request):
        print(f'{request.id}: {request.misatge}')
        return 'Done'


chatPrivadoService = ChatPrivadoService()
