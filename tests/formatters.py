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
        + (" sound" if model.play_sound else "muted")
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


async def str_scene_multiline(scene, indent, show_nodes=True, as_tree=False):
    if not show_nodes:
        nodes = ""
    elif not as_tree:
            nodes = (
                "\n|     +- "
                + ("\n" + indent + "|     +- ").join(str_node(node) for node in scene.nodes)
            )
    else:
        root_nodes = await scene.get_root_nodes()
        sub_item_strs = [
            str(await str_node_tree_multiline(node, indent + "|"))
            for node in root_nodes
            ]
        nodes = ("\n" +
            "".join(sub_item_strs)
        )

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


async def str_node_tree_multiline(node, indent):
    first_line = indent + "    +- " + str_node(node) + "\n"
    if node.scene_node_type == TSceneNodeType.ITEM:
        return first_line

    sub_nodes = await node.get_nodes()
    trailing_lines = (

         "".join(
            [(await str_node_tree_multiline(sub_node, indent + "    |")) for sub_node in sub_nodes]
        )
    )
    return first_line + trailing_lines
