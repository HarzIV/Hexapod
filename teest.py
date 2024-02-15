def transform_tuple(tuple_of_classes):
    return tuple(''.join((class_str[i].capitalize() if i == 0 or not class_str[i - 1].isalpha() else class_str[i]) for i in range(len(class_str))).replace('_', ' ') for class_name in tuple_of_classes for class_str in [class_name.__name__])

# Example usage:
class main_page_home:
    pass

class main_page_about_us:
    pass

class sidebar:
    pass

class footer:
    pass

class main_page_contact_us:
    pass

class other_page_services:
    pass

classes_tuple = (main_page_home, main_page_about_us, sidebar, footer, main_page_contact_us, other_page_services)
transformed_tuple = transform_tuple(classes_tuple)
print(transformed_tuple)
