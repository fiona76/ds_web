from pathlib import Path
import os


def main():
    if os.getenv("APP_TEST_MODE") == "1":
        return

    from trame.app import get_server
    from trame.ui.vuetify import SinglePageWithDrawerLayout
    from trame.widgets import vuetify, vtk

    import vtk

    server = get_server(client_type="vue2")
    state, ctrl = server.state, server.controller

    state.file_path = ""
    state.status = "Select a .vtu file to load"

    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.1, 0.12, 0.15)

    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    @state.change("file_path")
    def _validate_path(file_path, **_):
        path = Path(file_path) if file_path else None
        if not path or not path.exists():
            state.status = "File does not exist"
            return
        if path.suffix.lower() != ".vtu":
            state.status = "Please select a .vtu file"
            return
        state.status = "Ready to load"

    def load_vtu():
        path = Path(state.file_path)
        if not path.exists() or path.suffix.lower() != ".vtu":
            state.status = "Please select a valid .vtu file"
            return

        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(str(path))
        reader.Update()

        geometry = vtk.vtkGeometryFilter()
        geometry.SetInputConnection(reader.GetOutputPort())

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputConnection(geometry.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        renderer.RemoveAllViewProps()
        renderer.AddActor(actor)
        renderer.ResetCamera()

        render_window.Render()
        ctrl.view_update()
        state.status = f"Loaded {path.name}"

    ctrl.load_vtu = load_vtu

    with SinglePageWithDrawerLayout(server) as layout:
        layout.title.set_text("VTU Viewer")

        with layout.drawer:
            vuetify.VTextField(
                v_model=("file_path", ""),
                label="VTU file path",
                hint="Absolute or relative path on the server",
                persistent_hint=True,
                clearable=True,
                dense=True,
            )
            vuetify.VBtn("Load", click=ctrl.load_vtu, color="primary", class_="ma-2")
            vuetify.VAlert(v_model=("status", ""), type="info", dense=True)

        with layout.content:
            with vuetify.VContainer(fluid=True, class_="pa-0 fill-height"):
                vtk.VtkLocalView(render_window, ref="view")

    server.start()


if __name__ == "__main__":
    main()
