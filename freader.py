import sys


def read_file():
    # if len(sys.argv) == 3:
    #     print('Argumenty ok, vstupny subor:', str(sys.argv[1]), ', vystupny', str(sys.argv[2]))
    # else:
    #     print('Chyba nespravne spustenie skriptu: zadajte interpreter "meno suboru na konverziu" "meno vystupneho '
    #           'suboru"')
    #     sys.exit()
    #
    # filename = str(sys.argv[1])
    file = open('vstup1.txt', 'r')
    filecontent = file.read().splitlines()
    file.close()
    return filecontent


def write_result_to_file(result):
    # zapis vystupu
    filename = str(sys.argv[2])
    file = open(filename, 'w')
    file.write(result)
    file.close()
