# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory, ConversationState, TurnContext, UserState
from botbuilder.dialogs import Dialog
from helpers.dialog_helper import DialogHelper
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions


# class IcfesBot(ActivityHandler):
#     # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

#     async def on_members_added_activity(
#         self,
#         members_added: ChannelAccount,
#         turn_context: TurnContext
#     ):
#         return await self._send_welcome_message(turn_context)

#     async def _send_welcome_message(self, turn_context: TurnContext):
#         for member in turn_context.activity.members_added:
#             if member.id != turn_context.activity.recipient.id:
#                 await turn_context.send_activity(
#                     MessageFactory.text(
#                         f"Hola {member.name}, soy el Icfes-Bot. ¿Sabías que hay más de 7.000 programas de educación superior en Colombia? ¡Estoy aquí para ayudarte a elegir uno!"
#                     )
#                 )

#                 await self._send_suggested_actions(turn_context)
    
#     async def on_message_activity(self, turn_context: TurnContext):
#         text = turn_context.activity.text.lower()
#         response_text = self._process_input(text)

#         await turn_context.send_activity(MessageFactory.text(response_text))
#         return await self._send_suggested_actions(turn_context)

#     async def _send_suggested_actions(self, turn_context: TurnContext):
#         """
#         Creates and sends an activity with suggested actions to the user. When the user
#         clicks one of the buttons the text value from the "CardAction" will be displayed
#         in the channel just as if the user entered the text. There are multiple
#         "ActionTypes" that may be used for different situations.
#         """

#         reply = MessageFactory.text("¿Quieres que hablemos sobre tu paso a la educación superior?")

#         reply.suggested_actions = SuggestedActions(
#             actions=[
#                 CardAction(
#                     title="Si",
#                     type=ActionTypes.im_back,
#                     value="Si"
#                 ),
#                 CardAction(
#                     title="No",
#                     type=ActionTypes.im_back,
#                     value="No"
#                 )
#             ]
#         )
#         return await turn_context.send_activity(reply)

#     def _process_input(self, text: str):
#         if text == "si":
#             return f"Me alegro que quieras conversar."
#         if text == "no":
#             return f"OK, entiendo que no quieras conversar."

#         return "Please select a color from the suggested action choices"

class IcfesBot(ActivityHandler):
    """
    This Bot implementation can run any type of Dialog. The use of type parameterization is to allows multiple
    different bots to be run at different endpoints within the same project. This can be achieved by defining distinct
    Controller types each with dependency on distinct Bot types. The ConversationState is used by the Dialog system. The
    UserState isn't, however, it might have been used in a Dialog implementation, and the requirement is that all
    BotState objects are saved at the end of a turn.
    """

    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        if conversation_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. user_state is required but None was given"
            )
        if dialog is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have ocurred during the turn.
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )