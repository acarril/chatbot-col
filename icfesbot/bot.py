# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, TurnContext, MessageFactory
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions


class IcfesBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        return await self._send_welcome_message(turn_context)

    async def _send_welcome_message(self, turn_context: TurnContext):
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        f"Hola {member.name}, soy el Icfes-Bot. ¿Sabías que hay más de 7.000 programas de educación superior en Colombia? ¡Estoy aquí para ayudarte a elegir uno!"
                    )
                )

                await self._send_suggested_actions(turn_context)
    
    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text.lower()
        response_text = self._process_input(text)

        await turn_context.send_activity(MessageFactory.text(response_text))
        return await self._send_suggested_actions(turn_context)

    async def _send_suggested_actions(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """

        reply = MessageFactory.text("¿Quieres que hablemos sobre tu paso a la educación superior?")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Si",
                    type=ActionTypes.im_back,
                    value="Si"
                ),
                CardAction(
                    title="No",
                    type=ActionTypes.im_back,
                    value="No"
                )
            ]
        )
        return await turn_context.send_activity(reply)

    def _process_input(self, text: str):
        if text == "si":
            return f"Me alegro que quieras conversar."
        if text == "no":
            return f"OK, entiendo que no quieras conversar."

        return "Please select a color from the suggested action choices"

