from vispy.scene import SceneCanvas

import crysvue.visual.vispy as vp_visuals


class CrystalCanvas(SceneCanvas):

    def __init__(self, *args, bg_color='white', camera='arcball', **kwargs):
        super(CrystalCanvas, self).__init__(*args, **kwargs)
        self.unfreeze()
        self._elements = {k: dict() for k in ['atoms', 'bonds', 'axes', 'spins', 'unit_cell']}
        self.view = self.central_widget.add_view()
        self.view.camera = camera
        if bg_color is not None:
            self.view.bgcolor = bg_color
        self.freeze()

    @staticmethod
    def _generate_resize_event(view_box):
        def resize(event=None):
            new_size = int(event.size[1]/8)
            view_box.pos = (0, event.size[1] - new_size + 1)
            view_box.size = new_size, new_size
        return resize

    def add_element(self, key, element):
        self.unfreeze()
        self._elements[key][element.name] = element
        if key == 'axes':
            vb = self.central_widget.add_view(camera='arcball')
            view_size = int(self.view.size[1]/8)
            vb.size = (view_size, view_size)
            vb.pos = (0, self.view.height - view_size + 1)
            vb.border_color = 'white'
            vb.add(element)
            vb.camera.aspect = self.view.camera.aspect = 1  # no auto-scale
            vb.camera.link(self.view.camera, props=('center', 'fov', '_quaternion'))
            callback = self._generate_resize_event(vb)
            self.events.resize.connect(callback)
        else:
            element.parent = self.view.scene
        self.freeze()

    def remove_element(self, key, element):
        self.unfreeze()
        del self._elements[key][element.name]
        self.freeze()

    def on_draw(self, event):
        super().on_draw(event)

    @property
    def components(self):
        return {component_key: component for component_key, component in vp_visuals.__dict__.items() if isinstance(component, type) and component_key[0] != '_'}
