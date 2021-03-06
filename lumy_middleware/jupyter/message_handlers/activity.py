import logging

from kiara import get_version as get_kiara_version
from lumy_middleware import version
from lumy_middleware.jupyter.base import MessageHandler
from lumy_middleware.types.generated import (MsgExecutionState,
                                             MsgGetSystemInfo, MsgSystemInfo,
                                             State)

logger = logging.getLogger(__name__)


class ActivityHandler(MessageHandler):

    def initialize(self):
        self.context.processing_state_changed.subscribe(self._on_state_changed)

    def _on_state_changed(self, state: State):
        self.publisher.publish(MsgExecutionState(state))

    def _handle_GetSystemInfo(self, msg: MsgGetSystemInfo):
        return MsgSystemInfo(versions={
            'middleware': version,
            'backend': get_kiara_version()
        })
