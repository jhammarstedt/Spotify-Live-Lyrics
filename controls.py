    """
    The script we run to control the offset of the lyrics compared to the song
    Key I: Increase offset -- lyrics will appear later
    Key D: Decrease offset -- lyrics will appear earlier
    """
import json

while True:
    with open('config.json', 'r') as f:
        config = json.load(f)
    f.close()

    for k, v in config.items():
        print(k,': ', v)

    option = input('Selection ')

    if option == 'i':
        config['offset']+=0.25
        print('Offset increased')
    elif option == 'd':
        config['offset']-=0.25
        print('Offset decreased')
    else:
        print()

    with open('config.json', 'w') as f:
        json.dump(config, f)