from google_images import main

bird_list_file = open('llista_ocells_de_catalunya.txt', 'r')
species = bird_list_file.readlines()
 

for i, line in enumerate(species, start=1):

    normalized_line = line.strip()
    scientific_name = normalized_line.split(" (")[1].split(")")[0]
    catalan_name = normalized_line.split(" (")[0]

    print("Specie {}: {} ({})".format(i, catalan_name, scientific_name))

    main(scientific_name, catalan_name, 100)