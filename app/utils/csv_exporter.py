from flask import Response


class CsvExporter:

    @staticmethod
    def exportar_inscricoes(inscricoes):
        def gerar():
            yield 'ID,Nome,Telefone,Cidade,Mensagem,Data\n'

            for i in inscricoes:
                data = i.data_cadastro.strftime('%d/%m/%Y') if i.data_cadastro else ''
                msg = (i.mensagem or '').replace('\n', ' ').replace('\r', '')

                yield f"{i.id},{i.nome},{i.telefone},{i.cidade},{msg},{data}\n"

        return Response(
            gerar(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=inscricoes.csv'}
        )