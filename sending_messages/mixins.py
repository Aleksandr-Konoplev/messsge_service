# noinspection PyMethodMayBeStatic,PyUnresolvedReferences
class MenuActiveMixin:
    """
    Добавляет в контекст список URL для пунктов меню,
    чтобы подсвечивать активный элемент.
    """
    menu_urls = {
        'mailings': [
            'mailings_list',
            'mailing_detail',
            'mailing_create',
            'mailing_update',
            'mailing_delete',
        ],
        'recipients': [
            'recipients_list',
            'recipient_detail',
            'recipient_create',
            'recipient_update',
            'recipient_delete',
        ],
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu_urls'] = self.menu_urls
        return context
