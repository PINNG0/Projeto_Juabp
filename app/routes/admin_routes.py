from flask import Blueprint, render_template, request, redirect, url_for

from app.services.evento_service import EventoService
from app.services.inscricao_service import InscricaoService
from app.services.edicao_service import EdicaoService
from app.utils.csv_exporter import CsvExporter


from app.repositories.evento_repository import EventoRepository
from app.repositories.edicao_repository import EdicaoRepository

from app.utils.auth_guard import login_required, admin_required


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin')
@login_required
@admin_required
def admin():
    return render_template(
        'admin.html',
        inscritos=InscricaoService.obter_todas(),
        eventos_admin=EventoService.listar_eventos()
    )


@admin_bp.route('/admin/deletar/<int:id>', methods=['POST'])
@login_required
@admin_required
def deletar_inscricao(id):
    InscricaoService.deletar_inscricao(id)
    return redirect(url_for('admin.admin'))


@admin_bp.route('/admin/exportar')
@login_required
@admin_required
def exportar_csv():
    return CsvExporter.exportar_inscricoes(
        InscricaoService.obter_todas()
    )


@admin_bp.route('/admin/evento/novo', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_evento_novo():
    if request.method == 'POST':
        EventoService.criar_evento(
            nome=request.form.get('nome', '').strip(),
            categoria=request.form.get('categoria', '').strip(),
            introducao=request.form.get('introducao', '').strip(),
            alinhamento=request.form.get('alinhamento', '').strip(),
            texto_secundario=request.form.get('texto_secundario', '').strip(),
            banner_file=request.files.get('banner_file'),
            banner_url=request.form.get('banner_url', '').strip(),
            corpo_file=request.files.get('corpo_file'),
            corpo_url=request.form.get('corpo_url', '').strip()
        )
        return redirect(url_for('admin.admin'))

    return render_template('admin_evento_form.html')


@admin_bp.route('/admin/evento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_evento_editar(id):
    if request.method == 'POST':
        EventoService.editar_evento(
            id,
            nome=request.form.get('nome', '').strip(),
            categoria=request.form.get('categoria', '').strip(),
            introducao=request.form.get('introducao', '').strip(),
            alinhamento=request.form.get('alinhamento', '').strip(),
            texto_secundario=request.form.get('texto_secundario', '').strip(),
            banner_file=request.files.get('banner_file'),
            banner_url=request.form.get('banner_url', '').strip(),
            corpo_file=request.files.get('corpo_file'),
            corpo_url=request.form.get('corpo_url', '').strip()
        )
        return redirect(url_for('admin.admin'))

    evento = EventoRepository.buscar_por_id(id)

    return render_template(
        'admin_evento_editar.html',
        evento=evento.to_dict()  # Olha que beleza, chamando direto do objeto!
    )


@admin_bp.route('/admin/evento/deletar/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_evento_deletar(id):
    EventoService.deletar_evento(id)
    return redirect(url_for('admin.admin'))


@admin_bp.route('/admin/evento/<int:evento_id>/edicoes')
@login_required
@admin_required
def admin_edicoes(evento_id):
    return render_template(
        'admin_edicoes.html',
        evento=EventoRepository.buscar_por_id(evento_id),
        edicoes=EdicaoService.obter_por_evento(evento_id)
    )


@admin_bp.route('/admin/evento/<int:evento_id>/edicao/nova', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edicao_nova(evento_id):
    if request.method == 'POST':
        EdicaoService.criar_edicao(
            evento_id=evento_id,
            ano=request.form.get('ano', type=int),
            tema=request.form.get('tema', '').strip(),
            local=request.form.get('local', '').strip(),
            descricao=request.form.get('descricao', '').strip(),
            capa_file=request.files.get('capa_file'),
            capa_url=request.form.get('capa_url', '').strip(),
            link_nomes=request.form.getlist('link_nome[]'),
            link_urls=request.form.getlist('link_url[]')
        )
        return redirect(url_for('admin.admin_edicoes', evento_id=evento_id))

    return render_template(
        'admin_edicao_form.html',
        evento=EventoRepository.buscar_por_id(evento_id)
    )


@admin_bp.route('/admin/edicao/deletar/<int:id>', methods=['POST'])
@login_required
@admin_required
def admin_edicao_deletar(id):
    edicao = EdicaoRepository.sa_objeto_id(id)
    evento_id = edicao.evento_id

    EdicaoService.deletar_edicao(id)

    return redirect(
        url_for('admin.admin_edicoes', evento_id=evento_id)
    )