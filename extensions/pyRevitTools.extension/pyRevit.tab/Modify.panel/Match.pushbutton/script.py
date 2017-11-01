from pyrevit import revit, DB, UI
from pyrevit import script


__doc__ = 'pick the source object that has the element graphics override '\
          'you like to match to, and then pick the destination objects '\
          'one by one and this tool will match the graphics.'\
          '\n\nShift-Click: Shows Match Config window.'


my_config = script.get_config()


def setup_dim_overrides_per_config(from_dim, to_dim):
    if my_config.dim_override:
        to_dim.ValueOverride = from_dim.ValueOverride
    try:
        if my_config.dim_textposition:
            to_dim.TextPosition = to_dim.Origin \
                                  - (from_dim.Origin - from_dim.TextPosition)
    except Exception:
        pass

    if my_config.dim_above:
        to_dim.Above = from_dim.Above
    if my_config.dim_below:
        to_dim.Below = from_dim.Below
    if my_config.dim_prefix:
        to_dim.Prefix = from_dim.Prefix
    if my_config.dim_suffix:
        to_dim.Suffix = from_dim.Suffix


def setup_style_per_config(from_style, to_style):
    if my_config.halftone:
        to_style.SetHalftone(from_style.Halftone)

    if my_config.transparency:
        to_style.SetSurfaceTransparency(from_style.Transparency)

    if my_config.proj_line_color:
        to_style.SetProjectionLineColor(from_style.ProjectionLineColor)

    if my_config.proj_line_pattern:
        to_style.SetProjectionLinePatternId(from_style.ProjectionLinePatternId)

    if my_config.proj_line_weight:
        to_style.SetProjectionLineWeight(from_style.ProjectionLineWeight)

    if my_config.proj_fill_color:
        to_style.SetProjectionFillColor(from_style.ProjectionFillColor)

    if my_config.proj_fill_pattern:
        to_style.SetProjectionFillPatternId(from_style.ProjectionFillPatternId)

    if my_config.proj_fill_pattern_visibility:
        to_style.SetProjectionFillPatternVisible(
            from_style.IsProjectionFillPatternVisible
            )

    if my_config.cut_line_color:
        to_style.SetCutLineColor(from_style.CutLineColor)

    if my_config.cut_line_pattern:
        to_style.SetCutLinePatternId(from_style.CutLinePatternId)

    if my_config.cut_line_weight:
        to_style.SetCutLineWeight(from_style.CutLineWeight)

    if my_config.cut_fill_color:
        to_style.SetCutFillColor(from_style.CutFillColor)

    if my_config.cut_fill_pattern:
        to_style.SetCutFillPatternId(from_style.CutFillPatternId)

    if my_config.cut_fill_pattern_visibility:
        to_style.SetCutFillPatternVisible(from_style.IsCutFillPatternVisible)


def get_source_style(element_id):
    # get style of selected element
    from_style = revit.doc.ActiveView.GetElementOverrides(element_id)
    # make a new clean element style
    src_style = DB.OverrideGraphicSettings()
    # setup a new style per config and borrow from the selected element's style
    setup_style_per_config(from_style, src_style)
    return src_style


def pick_and_match_dim_overrides(src_dim_id):
    src_dim = revit.doc.GetElement(src_dim_id)
    while True:
        try:
            dest_dim = revit.doc.GetElement(
                revit.uidoc.Selection.PickObject(
                    UI.Selection.ObjectType.Element,
                    'Pick dimensions to match their overrides.'))

            if isinstance(dest_dim, DB.Dimension):
                with revit.Transaction('Match Dimension Overrides'):
                    setup_dim_overrides_per_config(src_dim, dest_dim)
        except Exception:
            break


def pick_and_match_styles(src_style):
    while True:
        try:
            dest_element = revit.doc.GetElement(
                revit.uidoc.Selection.PickObject(
                    UI.Selection.ObjectType.Element,
                    'Pick objects to change their graphic overrides.'))

            with revit.Transaction('Match Graphics Overrides'):
                revit.activeview.SetElementOverrides(dest_element.Id,
                                                     src_style)
        except Exception:
            break


# fixme: modify to remember source style
try:
    source_element = revit.doc.GetElement(
        revit.uidoc.Selection.PickObject(
            UI.Selection.ObjectType.Element,
            'Pick source object.')
        )

    if isinstance(source_element, DB.Dimension):
        pick_and_match_dim_overrides(source_element.Id)
    else:
        source_style = get_source_style(source_element.Id)
        pick_and_match_styles(source_style)
except Exception:
    pass
