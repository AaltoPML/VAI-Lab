from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from vai_lab.Data.xml_handler import XML_handler


class XMLReloadTest(unittest.TestCase):
    def setUp(self):
        workdir = TemporaryDirectory()
        self.addCleanup(workdir.cleanup)
        self.workflow = Path(workdir.name) / "workflow.xml"

    def test_reloading_keeps_same_type_modules_separate(self):
        self.workflow.write_text(
            """
            <pipeline>
                <Modelling name="first">
                    <plugin type="RidgeRegression">
                        <options><alpha>0.001</alpha></options>
                    </plugin>
                </Modelling>
                <Modelling name="second">
                    <plugin type="RidgeRegression"><options /></plugin>
                </Modelling>
            </pipeline>
            """,
            encoding="utf-8",
        )
        handler = XML_handler(str(self.workflow))
        modules = handler.loaded_modules

        handler.load_XML(None)

        self.assertIs(handler.loaded_modules, modules)
        self.assertEqual(modules["first"]["plugin"]["options"], {"alpha": 0.001})
        self.assertEqual(modules["second"]["plugin"]["options"], {})

    def test_reload_reflects_saved_changes_and_removals(self):
        self.workflow.write_text(
            """
            <pipeline>
                <Modelling name="first">
                    <plugin type="RidgeRegression">
                        <options><alpha>0.001</alpha><fit_intercept>False</fit_intercept></options>
                    </plugin>
                </Modelling>
                <Modelling name="removed" />
            </pipeline>
            """,
            encoding="utf-8",
        )
        handler = XML_handler(str(self.workflow))
        self.workflow.write_text(
            """
            <pipeline>
                <Modelling name="first">
                    <plugin type="RidgeRegression">
                        <options><alpha>0.02</alpha></options>
                    </plugin>
                </Modelling>
            </pipeline>
            """,
            encoding="utf-8",
        )

        handler.load_XML(None)

        self.assertEqual(list(handler.loaded_modules), ["first"])
        self.assertEqual(
            handler.loaded_modules["first"]["plugin"]["options"], {"alpha": 0.02}
        )

    def test_explicit_gui_merge_retains_preselected_data(self):
        self.workflow.write_text(
            '<pipeline><Initialiser name="Initialiser" />'
            '<Modelling name="first" /></pipeline>',
            encoding="utf-8",
        )
        data_file = self.workflow.with_name("measurements.csv")
        data_file.write_text("observation\n1\n", encoding="utf-8")
        handler = XML_handler()
        handler.new_config_file()
        handler.append_input_data("X", str(data_file), save_dir_as_relative=False)

        handler.load_XML(str(self.workflow), merge=True)

        self.assertEqual(handler.data_to_load(), {"X": data_file.as_posix()})
        self.assertIn("first", handler.loaded_modules)
