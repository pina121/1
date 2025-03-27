from rembg import remove
input_path = input('Your File Name: ')
output_path = 'output.png'
with open(input_path, 'rb') as i:
    with open(output_path, 'wb') as o:
        input_image = i.read()
        output = remove(input_image)
        o.write(output)
