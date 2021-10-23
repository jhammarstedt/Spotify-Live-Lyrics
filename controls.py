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