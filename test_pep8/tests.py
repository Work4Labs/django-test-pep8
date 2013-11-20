import os

from django.conf import settings
from django.test import TestCase
import pep8


class CollectTestReport(pep8.BaseReport):

    def __init__(self, options):
        super(CollectTestReport, self).__init__(options)
        self.all_errors = []
        self._fmt = pep8.REPORT_FORMAT.get(options.format.lower(),
                                           options.format)

    def error(self, line_number, offset, text, check):
        code = super(CollectTestReport, self).error(line_number, offset,
                                                    text, check)
        if not code:
            return

        self.all_errors.append(self._fmt % {
            'path': self.filename,
            'row': self.line_offset + line_number, 'col': offset + 1,
            'code': code, 'text': text[5:],
        })
        return code


class PEP8Test(TestCase):

    def test_pep8(self):
        exclude = getattr(settings, "TEST_PEP8_EXCLUDE", [])
        ignore = getattr(settings, "TEST_PEP8_IGNORE", [])
        config_file = getattr(settings, "TEST_PEP8_CONFIG_FILE", None)

        pep8_style = pep8.StyleGuide(
            reporter=CollectTestReport, exclude=exclude,
            ignore=ignore, config_file=config_file
        )

        report = pep8_style.check_files(settings.TEST_PEP8_DIRS)

        if report.all_errors:
            raise AssertionError(
                "ERROR: PEP8 errors:\n%s" % "\n".join(report.all_errors)
            )
