bl_info = {
    "name": "Totally Tubular",
    "author": "llealloo",
    "version": (0, 1, 0),
    "blender": (2, 93, 1),
    "location": "View3D > Sidebar > Edit Tab / Edit Mode Context Menu",
    "description": "Apply averaged cross sectional weights following tubular topography. Start with edge of one end of the tube selected.",
    "warning": "",
    "doc_url": "https://github.com/llealloo/join-modifiers-and-shapes/",
    "category": "Mesh",
}

import bpy

class tube_weight(bpy.types.Operator):
    """Apply averaged cross sectional weights following tubular topography. Start with edge of one end of the tube selected."""
    bl_idname = "mesh.tube_weight"
    bl_label = "Tubularize Weights"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj)
    
    def execute(self, context):
        
        nl = ['L','Left','left']
        nr = ['R','Right','right']
        
        o = bpy.context.active_object
        bpy.ops.object.mode_set(mode = "OBJECT")                                            # put object in object mode to save selection
        initial_selected_verts = [v.index for v in o.data.vertices if v.select]             # initially selected vertices
        bpy.ops.object.mode_set(mode = "EDIT")
        
        vertex_group_list = o.vertex_groups[:]
        selected_verts = initial_selected_verts
        focused_verts = selected_verts
        totally_tubular = True                                                              # the glass is half full
        
        while totally_tubular:
            slice_totals = [0 for x in vertex_group_list]   # total weight value for each vertex group of the current slice, indices paired with vertex_group_list

            # get the total weights of all vertices in the focused slice
            for vi in focused_verts:
                v = o.data.vertices[vi]
                vertex_group_elements = v.groups            # VertexGroupElement is a collection, contains group (as vert group index) and weight (as float)
                for g in vertex_group_elements:
                    group = g.group
                    weight = g.weight
                    slice_totals[group] = slice_totals[group] + weight
                        
            # get the average
            slice_averages = [x/len(initial_selected_verts) for x in slice_totals]
            
            # do the weight painting operation
            bpy.ops.object.mode_set(mode = "OBJECT")
            for vg in vertex_group_list:
                vg.remove(focused_verts)
                vg.add(focused_verts, slice_averages[vg.index], 'REPLACE')
            bpy.ops.object.mode_set(mode = "EDIT")
            
            # store previous selection & grow selection
            previously_selected_verts = selected_verts
            bpy.ops.mesh.select_more()
            bpy.ops.object.mode_set(mode = "OBJECT")
            bpy.ops.object.mode_set(mode = "EDIT")
            
            # compare grown selection to previous selection and take the new ones as focused verts
            selected_verts = [v.index for v in o.data.vertices if v.select]
            focused_verts = [v for v in selected_verts if v not in previously_selected_verts]
            
            # if the number of focused verts matches the initial selection, the selection is probably growing along a tube
            totally_tubular = (len(focused_verts) == len(initial_selected_verts))
            
        return {'FINISHED'}
    
# ########################################
# ##### GUI and registration #############
# ########################################

class OBJECT_PT_tube_weight_panel(bpy.types.Panel):
    """Creates a Sub-Panel in the Property Area of the 3D View"""
    bl_label = "Totally Tubular"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Edit"
    bl_context = "mesh_edit"

    def draw(self, context):

        layout = self.layout
        layout.separator()
        row = layout.row()
        row.operator(tube_weight.bl_idname)
        
        layout.separator()

def register():
    bpy.utils.register_class(tube_weight)
    bpy.utils.register_class(OBJECT_PT_tube_weight_panel)


def unregister():
    bpy.utils.unregister_class(tube_weight)
    bpy.utils.unregister_class(OBJECT_PT_tube_weight_panel)


if __name__ == "__main__":
    register()
