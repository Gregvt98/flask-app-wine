from flask import Blueprint
from flask import Flask, render_template, request, jsonify

ontology_blueprint = Blueprint('ontology', __name__, template_folder='templates/ontology',
    static_folder='static')

@ontology_blueprint.route('/contents')
def get_contents():
    return render_template('contents.html')

@ontology_blueprint.route('/classes')
def get_classes_index():
    return render_template("classes.html")

@ontology_blueprint.route('/classes/<class_name>')
def get_class(class_name):
    return render_template(f"""classes/{class_name}.html""")

@ontology_blueprint.route('/objectproperties')
def get_objectproperties_index():
    return render_template(f"""objectproperties.html""")

@ontology_blueprint.route('objectproperties/<objectproperty_name>')
def get_objectproperty(objectproperty_name):
    return render_template(f"""objectproperties/{objectproperty_name}""")

@ontology_blueprint.route('/dataproperties')
def get_dataproperties_index():
    return render_template(f"""dataproperties.html""")

@ontology_blueprint.route('/dataproperties/<dataproperty_name>')
def get_dataproperty(dataproperty_name):
    return render_template(f"""dataproperties/{dataproperty_name}.html""")

@ontology_blueprint.route('/annotationproperties')
def get_annotationproperties_index():
    return render_template(f"""annotationproperties.html""")

@ontology_blueprint.route('/annotationproperties/<annotationproperty_name>')
def get_annotationproperty(annotationproperty_name):
    return render_template(f"""annotationproperties/{annotationproperty_name}.html""")

@ontology_blueprint.route('/individuals')
def get_individuals_index():
    return render_template(f"""individuals.html""")

@ontology_blueprint.route('individuals/<individual_name>')
def get_individual(individual_name):
    return render_template(f"""individuals/{individual_name}""")

@ontology_blueprint.route('/datatypes')
def get_datatypes_index():
    return render_template(f"""datatypes.html""")

@ontology_blueprint.route('/datatypes/<datatype_name>')
def get_datatype(datatype_name):
    return render_template(f"""datatypes/{datatype_name}.html""")

