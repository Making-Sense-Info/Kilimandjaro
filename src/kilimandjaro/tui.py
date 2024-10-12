from chromadb.api import ClientAPI
from chromadb.config import Settings
from textual import on
from textual.containers import Center, Middle
from kilimandjaro.source import (
    get_category_scheme_from_ddi,
    get_snomed_terms,
    snomed_random_query,
    snomed_tension_query,
)
import pathlib
import pprint
import chromadb
from textual.app import App, ComposeResult
from textual.widgets import (
    Button,
    ContentSwitcher,
    Footer,
    Header,
    Label,
    Markdown,
    Pretty,
    ProgressBar,
)
from kilimandjaro.models import State, IDs


class Kilimandjaro(App):
    TITLE = "Kilimandjaro"
    SUB_TITLE = "Querying concepts"
    state: State = State()
    client: ClientAPI

    def on_mount(self) -> None:
        # self.client = chromadb.PersistentClient()
        # self.settings = self.client.get_settings()
        pass

    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            yield Button("Setup DB", id=IDs.SETDB)
            yield Label(f"(waiting for DB to be set up)", id=IDs.INFO)
            yield Pretty({}, id=IDs.PRE)
            yield Button("Run", id=IDs.RUN, disabled=not self.state.db_setup)
            # yield ProgressBar(id=IDs.PROGRESS)
            yield Markdown("__Waiting for results__", id="md")
            yield Button("Exit", id=IDs.EXIT)

    @on(Button.Pressed, "#" + IDs.SETDB)
    def setdb_button_clicked(self) -> None:
        # TODO use __init__ ?
        self.client = chromadb.PersistentClient()
        label = self.query_one("#" + IDs.INFO, Label)
        pre = self.query_one("#" + IDs.PRE, Pretty)
        label.update(f"DB set")
        pre.update(self.client.list_collections())
        self.state.db_setup = True
        self.query_one("#" + IDs.RUN).disabled = False

    @on(Button.Pressed, "#" + IDs.RUN)
    async def run_button_clicked(self) -> None:
        if self.state.db_setup:
            questionnaire_cs = await get_category_scheme_from_ddi(
                pathlib.Path.cwd() / "dat" / "constances-questionnaire.xml"
            )
            snomed_terms = await get_snomed_terms(snomed_tension_query)
            collection = self.client.get_or_create_collection(name="terms")
            ids = [f"sno{i}" for i, _ in enumerate(snomed_terms)]
            # collection.add(documents=snomed_terms, ids=ids)
            results = collection.query(query_texts=questionnaire_cs, n_results=2)
            md_results = "__Results__\n"
            for i, e in enumerate(questionnaire_cs):
                md_results += f"  - _Constances_: {e} - _Snomed terms_:\n"
                for res in results["documents"][i]:
                    md_results += f"    - {res}\n"
                md_results += "\n"
            self.query_one("#md", Markdown).update(md_results)

    @on(Button.Pressed, "#" + IDs.EXIT)
    def on_exit_clicked(self) -> None:
        self.exit()


if __name__ == "__main__":
    kapp = Kilimandjaro()
    kapp.run()
