#-*- encoding=UTF-8 -*-
import sys
import xml.etree.cElementTree as ET
import sys
import xmltodict
from collections import OrderedDict
import pandas as pd
import xlwings as xw
import json



class ArxmlToXls:
    def __init__(self, arxmlFile):
        self.arxmlFile = arxmlFile
        self.lines = None        
        self.depth = 0
        self.arxml_to_dict()

    def arxml_to_dict(self):
        fd = open(self.arxmlFile)
        # print(">>> Processing {}".format(self.arxmlFile))
        self.arxml_dict = xmltodict.parse(fd.read())
        self.parse_topology()

    def foreach_containers(self, containers):
        self.depth+= 1
        containers_list = list()   
        if type(containers['ECUC-CONTAINER-VALUE']) != list:
            containers_list.append(containers['ECUC-CONTAINER-VALUE'])
        else:
            containers_list = containers['ECUC-CONTAINER-VALUE']
        # print('333', containers_list, type(containers_list))            
        for container in containers_list:
            container_root_name = container['SHORT-NAME']
            print('#'*(self.depth) + ' ' + container_root_name)
            if(container_root_name == 'TEST0_AD'):
                pass
            if 'SUB-CONTAINERS' not in container:
                # value_maps = ['DEFINITION-REF', 'PARAMETER-VALUES']
                value_maps = ['DEFINITION-REF']
                for value_map in value_maps:
                    if value_map in container:
                        definitions = container[value_map]
                        break
                    # print('#'*(self.depth+1), definitions['#text'])
                para_type_maps = ['REFERENCE-VALUES', 'PARAMETER-VALUES']

                values_dict = dict()
                for para_type in para_type_maps:
                    if para_type in container:
                        values_dict[para_type] = container[para_type]
                config_valules_dict = dict()
                for key, value in values_dict.items():
                    sub_value_type_maps = ['ECUC-REFERENCE-VALUE', 'ECUC-NUMERICAL-PARAM-VALUE', 'ECUC-TEXTUAL-PARAM-VALUE']
                    for sub_type in sub_value_type_maps:
                        if sub_type in value:
                            config_valules_dict[sub_type] = value[sub_type]
                for key, values in config_valules_dict.items():
                    values_list = list()
                    if type(values) != list:
                        values_list.append(values)
                    else:
                        values_list = values
                    for value in values_list:
                        # print(len(config_valules_dict), type(value), len(value))
                        definition = value['DEFINITION-REF']['#text']
                        try:
                            definition_value = value['VALUE-REF']['#text']
                        except:
                            definition_value = value['VALUE']
                        print('#'*(self.depth+1), definition)
                        print('#'*(self.depth+2), definition_value)
                        # print('depth = {0}'.format(self.depth))

            else:
                # self.depth+= 1
                sub_containers = container['SUB-CONTAINERS']
                # print('2', type(sub_containers))                
                self.foreach_containers(sub_containers)
        self.depth-= 1
    def get_mermaid(self):
        if isinstance(self.arxml_dict['AUTOSAR']['AR-PACKAGES']['AR-PACKAGE']['ELEMENTS']['ECUC-MODULE-CONFIGURATION-VALUES']['CONTAINERS'], dict):
            # print('get containers')
            containers = self.arxml_dict['AUTOSAR']['AR-PACKAGES']['AR-PACKAGE']['ELEMENTS']['ECUC-MODULE-CONFIGURATION-VALUES']['CONTAINERS']
            #self.traverse_dict(containers)
            # print('1', type(containers))
            self.foreach_containers(containers)
            return


    def parse_topology(self):
        self.get_mermaid()


if __name__ == '__main__':
    file = sys.argv[1]
    # arFile = r'adc_test.arxml'
    arxmlObject = ArxmlToXls(file)
    pass



 