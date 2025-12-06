from pyslobs import MonitoringType, TSceneNodeType


def str_emonitoringtype(emt):
    return "No Monitoring" if emt == MonitoringType.NONE else (emt.name)


def str_ifader(ifader):
    return f"Fader(db={ifader.db}, deflection={ifader.deflection}, mul={ifader.mul})"


def str_iaudiosourcemodel_multiline(model, indent):
    return (
        indent
        + "+- Model:"
        + (" " + repr(model.name))
        + ("\n" + indent + "|    ")
        + (" Source id: " + model.source_id)
        + ("\n" + indent + "|    ")
        + (" muted " if model.muted else "")
        + (" Mixers: " + f"{model.audio_mixers}")
        + (" forced-mono" if model.force_mono else "")
        + (" mixer-hidden" if model.mixer_hidden else "")
        + f" sync-offset: {model.sync_offset}"
        + (" " + str_emonitoringtype(model.monitoring_type))
        + ("\n" + indent + "|    ")
        + " Fader:"
        + f" {model.fader.db}db"
        + f" def:{model.fader.deflection}"
        + f" mul:{model.fader.mul}"
        + "\n"
    )


def str_inotificationsettings(settings):
    return (
        "Notification Settings: "
        + ("enabled" if settings.enabled else "disabled")
        + " sound"
        if settings.play_sound
        else "no-sound"
    )


async def str_audiosource_multiline(audio_source, indent):
    model = await audio_source.get_model()
    return (
        indent
        + "+- AudioSource:"
        + "\n"
        + str_iaudiosourcemodel_multiline(model, indent + "| ")
    )


async def str_audiosources_multiline(audio_sources, indent):
    return "".join(
        [(await str_audiosource_multiline(source, "  ")) for source in audio_sources]
    )


def str_notificationmodel_multiline(model, indent):
    return (
        indent
        + "+- Notification"
        + f"({model.id}):"
        + (" " + model.type.name + "/" + model.subtype.name)
        + (" " + model.message)
        + ("\n" + indent + "|    ")
        + ("unread" if model.unread else "read")
        + f" date: {model.date}"
        + f" lifetime: {model.lifetime}"
        + ("\n" + indent + "|    ")
        + (f"action: {model.action}" if model.code else "no-action")
        + (f" code: {model.code}" if model.code else " no-code")
        + (f" data: {model.data}" if model.data else " no-data")
        + (" show-time" if model.show_time else "")
        + (" sound" if model.play_sound else " muted")
        + "\n"
    )


def str_notificationmodels_multiline(notifications, indent):
    return "".join(
        [
            (str_notificationmodel_multiline(notification, "  "))
            for notification in notifications
        ]
    )


def str_iperformancestate(state):
    return "CPU: %d%%, Bandwidth: %d, %d fps, %d dropped frames (%d%%)" % (
        state.cpu,
        state.bandwidth,
        state.frame_rate,
        state.number_dropped_frames,
        state.percentage_dropped_frames,
    )


def str_itransitionsservicestate(state):
    return "Studio-Mode" if state.studio_mode else "Direct-Mode"


async def str_scene_multiline(
    scene, indent, show_nodes=True, as_tree=False, folders_first=False
):
    if not show_nodes:
        nodes = ""
    elif not as_tree:
        nodes = "\n|     +- " + ("\n" + indent + "|     +- ").join(
            str_node(node) for node in scene.nodes
        )
    else:
        node_formatter = (
            str_node_tree_multiline_folders_first
            if folders_first
            else str_node_tree_multiline
        )
        root_nodes = await scene.get_root_nodes()
        sub_item_strs = [
            str(await node_formatter(node, indent + "|")) for node in root_nodes
        ]
        nodes = "\n" + "".join(sub_item_strs)

    return (
        indent
        + "+- Scene:"
        + (" " + repr(scene.name))
        + ("\n" + indent + "|    ")
        + ("Source id: " + scene.source_id)
        + (" Id: " + scene.id)
        + nodes
    )


def str_node(node):
    return (
        node.__class__.__name__
        + ":"
        + (" " + node.name)
        + (" (" + node.scene_node_type.name + ")")
        + (" Id: " + node.id_)
        + (" Node-Id: " + str(node.node_id))
        + (" Parent-Id: " + node.parent_id)
        + (" Scene-Id: " + node.scene_id)
        + (" Source-Id: " + str(node.source_id))
    )

async def str_nodeitem(nodeitem, indent, extended=False):
    summary_line = indent + "    +- " + str_node(nodeitem) + "\n"
    if extended:
        visibility_line =  (
            indent + "     | " +
            ("locked " if nodeitem.locked else "unlocked") +
            ("stream-invisible " if not nodeitem.stream_visible else "") +
            ("rec-invisible " if not nodeitem.recording_visible else "") +
            ("rec-invisible " if not nodeitem.visible else "") +
            "\n")

        crop_line = (
            indent + "     | " +
            ("crop: (t:%s l:%s b:%s r:%s) " % (
                nodeitem.transform.crop.top,
                nodeitem.transform.crop.left,
                nodeitem.transform.crop.bottom,
                nodeitem.transform.crop.right,
            )) +
            "\n")

        position_line = (
            indent + "     | " +
            ("pos: (x:%s y:%s) rot: %s scale: %s" % (
                nodeitem.transform.position.x,
                nodeitem.transform.position.y,
                nodeitem.transform.rotation,
                nodeitem.transform.scale,
            )) +
            "\n")

        return summary_line + visibility_line + crop_line + position_line
    else:
        return summary_line


async def str_node_tree_multiline(node, indent, extended=False):
    if node.scene_node_type == TSceneNodeType.ITEM:
        return await str_nodeitem(node, indent, extended)

    # Must be an ITEMFOLDER

    heading_line = indent + "    +- " + await str_node(node) + "\n"

    sub_nodes = await node.get_nodes()
    trailing_lines = "".join(
        [
            (await str_node_tree_multiline(sub_node, indent + "    |", extended))
            for sub_node in sub_nodes
        ]
    )
    return heading_line + trailing_lines


async def str_node_tree_multiline_folders_first(node, indent):
    first_line = indent + "    +- " + str_node(node) + "\n"
    if node.scene_node_type == TSceneNodeType.ITEM:
        return first_line

    sub_nodes = await node.get_folders()
    folder_lines = "".join(
        [
            (await str_node_tree_multiline_folders_first(sub_node, indent + "    |"))
            for sub_node in sub_nodes
        ]
    )

    sub_nodes = await node.get_items()
    item_lines = "".join(
        [
            (await str_node_tree_multiline_folders_first(sub_node, indent + "    |"))
            for sub_node in sub_nodes
        ]
    )

    return first_line + folder_lines + item_lines


async def str_source_multiline(source, indent):
    return (
        indent
        + "+- Source:"
        + (" " + repr(source.name))
        + (" " + repr(source.resource_id))
        + (" " + repr(source.source_id))
        + ("\n" + indent + "|    ")
        + source.type_
        + f" {'A' if source.audio else ''}{'(muted)' if source.muted else''}"
        + f"{'V' if source.video else ''}({source.width}x{source.height})"
        + f" ch:{source.channel}"
        + f"{' do-not-duplicate' if source.do_not_duplicate else''}"
        + ("\n" + indent + "|      ")
        + ("+- Model: " + str(await source.get_model()))
        + ("\n" + indent + "|      ")
        + ("+- Settings: " + str(await source.get_settings()))
    )


def str_scenecollectionschemascene_multiline(sceneref, indent):
    return indent + "+- Scene Reference: " + sceneref["name"]


def str_scenecollectionschemasources_multiline(sourceref, indent):
    return (
        indent
        + "+- Source reference list\n"
        + "\n".join(
            str_scenecollectionschemasource_multiline(subsourceref, indent + "|   ")
            for subsourceref in sourceref
        )
    )


def str_scenecollectionschemasource_multiline(sourceref, indent):
    return (
        indent
        + "+- Source Reference:"
        + sourceref["name"]
        + " ("
        + sourceref["type"]
        + ")"
    )


def str_scenecollectionschema_multiline(schema, indent):
    return (
        indent
        + "+- SceneCollectionSchema:"
        + schema.name
        + "\n"
        + "\n".join(
            str_scenecollectionschemascene_multiline(sceneref, indent + "|    ")
            for sceneref in schema.scenes
        )
        + "\n"
        + "\n".join(
            str_scenecollectionschemasources_multiline(sourceref, indent + "|    ")
            for sourceref in schema.sources
        )
    )
