from ape import tasks
import os
import json
import sys
import shutil

@tasks.register_helper
def get_cookiecutter_template_dir(template_name):
    import djpl_container_management
    tpl_dir = '%s/cookiecutter_templates/%s' % (
        os.path.dirname(djpl_container_management.__file__),
        template_name
    )
    if os.path.isdir(tpl_dir):
        return tpl_dir
    else:
        raise Exception('cookiecutter template not found: ' + tpl_dir)


def get_location(doi):
    parts = doi.split(':')
    if len(parts) == 2:
        container_name, product_name = parts[0], parts[1]
        return (container_name, product_name)
    else:
        raise Exception('unable to parse context - format: <container_name>:<product_name>')


@tasks.register
def create_product(poi):
    '''
    Create a product <product_name> in <container_name>. The argument <poi> is in the form
    container_name:product_name
    '''
    container_name, product_name = get_location(poi)
    from cookiecutter.generate import generate_files
    import uuid
    template_dir = tasks.get_cookiecutter_template_dir('djpl_product')
    webapps = os.environ['APE_ROOT_DIR']
    container_dir = '%s/%s' % (webapps, container_name)

    if not os.path.isdir(container_dir):
        print 'ERROR: %s is not a valid container as it does not exist.' % container_dir
        return

    products_dir = container_dir + '/products'
    if not os.path.isdir(products_dir):
        print 'ERROR: %s must contain a "products" directory.' % container_dir
        return

    product_dir = products_dir + '/' + product_name
    if os.path.isdir(product_dir):
        print 'ERROR: the product "%s:%s" already exists. Choose another product name or delete this product and try again.' % (container_name, product_name)
        return

    generate_files(
        template_dir,
        context=dict(
            cookiecutter={
                'product_name': product_name,
                'product_dir': product_dir,
                'secret_key': str(uuid.uuid1())
            }
        ),
        output_dir=products_dir
    )
    print '*** Created product %s:%s' % (container_name, product_name)


@tasks.register
def create_container(container_name):
    '''
    Create a container <container_name>.
    '''
    from cookiecutter.generate import generate_files
    template_dir = tasks.get_cookiecutter_template_dir('djpl_container')
    webapps = os.environ['APE_ROOT_DIR']
    container_dir = '%s/%s' % (webapps, container_name)

    if os.path.isdir(container_dir):
        print 'ERROR: %s already exists.' % container_dir
        return

    generate_files(
        template_dir,
        context=dict(
            cookiecutter={
                'container_name': container_name,
            }
        ),
        output_dir=webapps
    )
    print '*** Created container %s' % (container_name)


@tasks.register
def create_feature(feature_name, container_name=None, location=None):
    '''
    Create a feature <feature_name>.

    If <location> and <container_name> is specified, an error is raised.
    If <location> is given the feature is created at that location(relative from current working directory)
    If <container_name> is given the feature is created in the "features" directory of the given container.
    If neither <location> nor <container_name> is given, the feature is created in the current container - if
    no container is active an error is raised.
    '''

    if location and container_name:
        print 'ERROR: combining container_name and location options is not supported.'
        sys.exit(1)

    if not location and not container_name:
        container_name = os.environ['CONTAINER_NAME']

    if container_name:
        location = os.path.join(tasks.get_container_dir(container_name), 'features')
    else:
        location = os.path.abspath(os.path.normpath(location))

    from cookiecutter.generate import generate_files
    from django_productline.context import PRODUCT_CONTEXT
    template_dir = tasks.get_cookiecutter_template_dir('djpl_feature')

    feature_dir = os.path.join(location, feature_name)
    if os.path.isdir(feature_dir):
        print 'ERROR: %s already exists.' % feature_dir
        return

    generate_files(
        template_dir,
        context=dict(
            cookiecutter={
                'feature_name': feature_name,
            }
        ),
        output_dir=location
    )
    print '*** Created feature %s in %s' % (feature_name, location)


def get_containers_location(poi):
    parts = poi.split(':')
    if len(parts) == 2:
        source_container, target_container = parts[0], parts[1]
        return (source_container, target_container)
    else:
        raise Exception('unable to parse context - format: <source_container>:<target_container>')

@tasks.register
def create_project_from(poi, exclude=''):
    '''
    This task copy a whole container except for _lib in container root, context.json and __data__ in all products and additionally excludes.
    The argument <poi> is in the form source_container:target_container
    The optional argument <exclude> is in the form a,b,c - seperate exclude files and dirs with ,
    '''
    apedir = os.environ['APE_ROOT_DIR']
    source_container, target_container = get_containers_location(poi)

    source_container_dir = '%s/%s' % (apedir, source_container)
    target_container_dir = '%s/%s' % (apedir, target_container)
    if not os.path.isdir(source_container_dir):
        print 'ERROR: %s is not a valid container as it does not exist.' % source_container_dir
        return

    products_dir = source_container_dir + '/products'
    if not os.path.isdir(products_dir):
        print 'ERROR: %s must contain a "products" directory.' % source_container_dir
        return

    if os.path.isdir(target_container_dir):
        print 'ERROR: Target Container %s already exist' % target_container_dir
        return


    exclude_list = ['_lib', '__data__', 'context.json', 'httpd'] + exclude.split(',')

    print 'copy from %s to %s ..... ' % (source_container_dir, target_container_dir)
    try:
        shutil.copytree(source_container_dir, target_container_dir, ignore=shutil.ignore_patterns(*exclude_list))
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            shutil.copy(source_container_dir, target_container_dir)
        else:
            print('ERROR: Directory not copied. Error: %s' % e)
            return
    print 'done - now start with ape install_cotainer %s' %  target_container
