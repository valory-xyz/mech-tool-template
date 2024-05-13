from mech_client.interact import interact, ConfirmationType

prompt_text = "Will ChatGPT-5 be presented before May 22nd 2024?"
agent_id = 6
tool_name = "prediction-online"
chain_config = "gnosis"
private_key_path="ethereum_private_key.txt"

result = interact(
    prompt=prompt_text,
    agent_id=agent_id,
    tool=tool_name,
    chain_config=chain_config,
    confirmation_type=ConfirmationType.ON_CHAIN,
    private_key_path=private_key_path
)

print(result)