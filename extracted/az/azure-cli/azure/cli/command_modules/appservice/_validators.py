# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import ipaddress


from azure.cli.core.azclierror import (InvalidArgumentValueError, ArgumentUsageError, RequiredArgumentMissingError,
                                       ResourceNotFoundError, ValidationError, MutuallyExclusiveArgumentError)
from azure.cli.core.commands.client_factory import get_mgmt_service_client, get_subscription_id
from azure.cli.core.commands.validators import validate_tags
from azure.mgmt.core.tools import is_valid_resource_id, parse_resource_id

from knack.log import get_logger

from ._appservice_utils import _generic_site_operation
from ._client_factory import web_client_factory
from .utils import (_normalize_sku, get_sku_tier, get_resource_name_and_group,
                    get_resource_if_exists, is_functionapp, is_logicapp, is_webapp, is_centauri_functionapp,
                    _normalize_location)

from .aaz.latest.network import ListServiceTags
from .aaz.latest.network.vnet import List as VNetList, Show as VNetShow
from ._constants import ACR_IMAGE_SUFFIX

logger = get_logger(__name__)


def validate_and_convert_to_int(flag, val):
    try:
        return int(val)
    except ValueError:
        raise ArgumentUsageError("{} is expected to have an int value.".format(flag))


def validate_range_of_int_flag(flag_name, value, min_val, max_val):
    value = validate_and_convert_to_int(flag_name, value)
    if min_val > value or value > max_val:
        raise ArgumentUsageError("Usage error: {} is expected to be between {} and {} (inclusive)".format(flag_name,
                                                                                                          min_val,
                                                                                                          max_val))
    return value


def validate_timeout_value(namespace):
    """Validates that zip deployment timeout is set to a reasonable min value"""
    if isinstance(namespace.timeout, int):
        if namespace.timeout <= 29:
            raise ArgumentUsageError('--timeout value should be a positive value in seconds and should be at least 30')


def validate_site_create(cmd, namespace):
    """Validate the SiteName that is being used to create is available
    This API requires that the RG is already created"""
    client = web_client_factory(cmd.cli_ctx)
    if isinstance(namespace.name, str) and isinstance(namespace.resource_group_name, str) \
            and isinstance(namespace.plan, str):
        resource_group_name = namespace.resource_group_name
        plan = namespace.plan
        if is_valid_resource_id(plan):
            parsed_result = parse_resource_id(plan)
            plan_info = client.app_service_plans.get(parsed_result['resource_group'], parsed_result['name'])
        else:
            plan_info = client.app_service_plans.get(resource_group_name, plan)
        if not plan_info:
            raise ResourceNotFoundError("The plan '{}' doesn't exist in the resource group '{}'".format(
                plan, resource_group_name))
        # verify that the name is available for create
        validation_payload = {
            "name": namespace.name,
            "type": "Microsoft.Web/sites",
            "location": plan_info.location,
            "properties": {
                "serverfarmId": plan_info.id
            }
        }
        validation = client.validate(resource_group_name, validation_payload)
        if validation.status.lower() == "failure" and validation.error.code != 'SiteAlreadyExists':
            raise ValidationError(validation.error.message)


def validate_ase_create(cmd, namespace):
    # Validate the ASE Name availability
    client = web_client_factory(cmd.cli_ctx)
    resource_type = 'Microsoft.Web/hostingEnvironments'
    if isinstance(namespace.name, str):
        name_validation = client.check_name_availability(namespace.name, resource_type)
        if not name_validation.name_available:
            raise ValidationError(name_validation.message)


def _validate_asp_sku(sku, app_service_environment, zone_redundant):
    supported_skus = ['PREMIUMV2', 'PREMIUMV3', 'PREMIUMMV3', 'PREMIUM0V3', 'PREMIUMV4', 'PREMIUMMV4', 'ISOLATEDV2', 'ISOLATEDMV2']  # pylint: disable=line-too-long
    if zone_redundant and get_sku_tier(sku).upper() not in supported_skus:
        raise ValidationError("Zone redundancy cannot be enabled for sku {}".format(sku))
    # Isolated SKU is supported only for ASE
    if sku.upper() in ['I1V2', 'I2V2', 'I3V2', 'I4V2', 'I5V2', 'I6V2', 'I1MV2', 'I2MV2', 'I3MV2', 'I4MV2', 'I5MV2']:
        if not app_service_environment:
            raise ValidationError("The pricing tier 'Isolated' is not allowed for this app service plan. "
                                  "Use this link to learn more: "
                                  "https://learn.microsoft.com/azure/app-service/overview-hosting-plans")
    else:
        if app_service_environment:
            raise ValidationError("Only pricing tier 'IsolatedV2' and 'IsolatedMV2' is allowed in this "
                                  "app service plan. Use this link to "
                                  "learn more: https://learn.microsoft.com/azure/app-service/overview-hosting-plans")


def validate_asp_create(namespace):
    validate_tags(namespace)
    sku = _normalize_sku(namespace.sku)
    _validate_asp_sku(sku, namespace.app_service_environment, namespace.zone_redundant)
    if namespace.is_linux and namespace.hyper_v:
        raise MutuallyExclusiveArgumentError('Usage error: --is-linux and --hyper-v cannot be used together.')


def validate_functionapp_asp_create(namespace):
    validate_tags(namespace)
    sku = _normalize_sku(namespace.sku)
    tier = get_sku_tier(sku)
    _validate_asp_sku(sku=sku, app_service_environment=None, zone_redundant=namespace.zone_redundant)
    if namespace.max_burst is not None:
        if tier.lower() != "elasticpremium":
            raise ArgumentUsageError("--max-burst is only supported for Elastic Premium (EP) plans")


def validate_functionapp_on_containerapp_site_config_set(cmd, namespace):
    resource_group_name = namespace.resource_group_name
    name = namespace.name
    if is_centauri_functionapp(cmd, resource_group_name, name):
        raise ValidationError(
            "Invalid command. This is not supported for Azure Functions on Azure Container app environments.",
            "Please use the following command instead: az functionapp config container set")


def validate_functionapp_on_containerapp_container_settings_delete(cmd, namespace):
    resource_group_name = namespace.resource_group_name
    name = namespace.name
    if is_centauri_functionapp(cmd, resource_group_name, name):
        raise ValidationError(
            "Invalid command. This is currently not supported for Azure Functions on Azure Container app environments.",
            "Please use the following command instead: az functionapp config appsettings set")
    validate_functionapp_on_flex_plan(cmd, namespace)


def validate_functionapp_on_containerapp_update(cmd, namespace):
    resource_group_name = namespace.resource_group_name
    name = namespace.name
    if is_centauri_functionapp(cmd, resource_group_name, name):
        raise ValidationError(
            "Invalid command. This is currently not supported for Azure Functions on Azure Container app environments.",
            "Please use either 'az functionapp config appsettings set' or 'az functionapp config container set'")


def validate_functionapp_on_containerapp_site_config_show(cmd, namespace):
    resource_group_name = namespace.resource_group_name
    name = namespace.name
    if is_centauri_functionapp(cmd, resource_group_name, name):
        raise ValidationError(
            "Invalid command. This is not supported for Azure Functions on Azure Container app environments.",
            "Please use the following command instead: az functionapp config container show")


def validate_functionapp_on_flex_plan(cmd, namespace):
    resource_group_name = namespace.resource_group_name
    name = _get_app_name(namespace)
    functionapp = _generic_site_operation(cmd.cli_ctx, resource_group_name, name, 'get')
    if functionapp.server_farm_id is None:
        return
    parsed_plan_id = parse_resource_id(functionapp.server_farm_id)
    client = web_client_factory(cmd.cli_ctx)
    plan_info = client.app_service_plans.get(parsed_plan_id['resource_group'], parsed_plan_id['name'])
    if plan_info is None:
        raise ResourceNotFoundError('Could not determine the current plan of the functionapp')
    if plan_info.sku.tier == 'FlexConsumption':
        raise ValidationError('Invalid command. This is not currently supported for Azure Functions '
                              'on the Flex Consumption plan.')


def validate_is_flex_functionapp(cmd, namespace):
    resource_group_name = namespace.resource_group_name
    name = namespace.name
    functionapp = _generic_site_operation(cmd.cli_ctx, resource_group_name, name, 'get')
    if functionapp.server_farm_id is None:
        raise ValidationError('This command is only valid for Azure Functions on the FlexConsumption plan.')
    parsed_plan_id = parse_resource_id(functionapp.server_farm_id)
    client = web_client_factory(cmd.cli_ctx)
    plan_info = client.app_service_plans.get(parsed_plan_id['resource_group'], parsed_plan_id['name'])
    if plan_info is None:
        raise ResourceNotFoundError('Could not determine the current plan of the functionapp')
    if plan_info.sku.tier.lower() != 'flexconsumption':
        raise ValidationError('This command is only valid for Azure Functions on the FlexConsumption plan.')


def validate_app_exists(cmd, namespace):
    app = namespace.name
    resource_group_name = namespace.resource_group_name
    slot = namespace.slot
    app = _generic_site_operation(cmd.cli_ctx, resource_group_name, app, 'get', slot)
    if not app:
        raise ResourceNotFoundError("'{}' app not found in ResourceGroup '{}'".format(app, resource_group_name))


def validate_functionapp_on_containerapp_vnet_add(cmd, namespace):
    validate_functionapp_on_containerapp_vnet(cmd, namespace)
    validate_add_vnet(cmd, namespace)


def validate_functionapp_on_containerapp_vnet(cmd, namespace):
    resource_group_name = namespace.resource_group_name
    name = namespace.name
    if is_centauri_functionapp(cmd, resource_group_name, name):
        raise ValidationError(
            'Unsupported operation on function app.',
            'Please set virtual network configuration for the function app at Container app environment level.')


def validate_add_vnet(cmd, namespace):
    from azure.core.exceptions import ResourceNotFoundError as ResNotFoundError

    resource_group_name = namespace.resource_group_name
    vnet_identifier = namespace.vnet
    name = namespace.name
    slot = namespace.slot

    if is_valid_resource_id(vnet_identifier):
        current_sub_id = get_subscription_id(cmd.cli_ctx)
        parsed_vnet = parse_resource_id(vnet_identifier)

        vnet_sub_id = parsed_vnet['subscription']
        vnet_group = parsed_vnet['resource_group']
        vnet_name = parsed_vnet['name']

        cmd.cli_ctx.data['subscription_id'] = vnet_sub_id
        vnet_loc = VNetShow(cli_ctx=cmd.cli_ctx)(command_args={
            "name": vnet_name,
            "resource_group": vnet_group
        })["location"]
        cmd.cli_ctx.data['subscription_id'] = current_sub_id
    else:
        try:
            vnet_loc = VNetShow(cli_ctx=cmd.cli_ctx)(command_args={
                "name": vnet_identifier,
                "resource_group": namespace.resource_group_name
            })["location"]
        except ResNotFoundError:
            vnets = VNetList(cli_ctx=cmd.cli_ctx)(command_args={})
            vnet_loc = ''
            for v in vnets:
                if vnet_identifier == v["name"]:
                    vnet_loc = v["location"]
                    break

    if not vnet_loc:
        # Fall back to back end validation
        logger.warning("Failed to fetch vnet. Skipping location validation.")
        return

    webapp = _generic_site_operation(cmd.cli_ctx, resource_group_name, name, 'get', slot)

    webapp_loc = _normalize_location(cmd, webapp.location)
    vnet_loc = _normalize_location(cmd, vnet_loc)

    if vnet_loc != webapp_loc:
        raise ValidationError("The app and the vnet resources are in different locations. "
                              "Cannot integrate a regional VNET to an app in a different region"
                              "Web app location: {}. Vnet location: {}".format(webapp_loc, vnet_loc))


def validate_ip_address(cmd, namespace):
    if namespace.ip_address is not None:
        _validate_ip_address_format(namespace)
        # For prevention of adding the duplicate IPs.
        if 'add' in cmd.name:
            _validate_ip_address_existence(cmd, namespace)


def validate_onedeploy_params(namespace):
    if namespace.src_path and namespace.src_url:
        raise MutuallyExclusiveArgumentError('Only one of --src-path and --src-url can be specified')

    if not namespace.src_path and not namespace.src_url:
        raise RequiredArgumentMissingError('Either of --src-path or --src-url must be specified')

    if namespace.src_url and not namespace.artifact_type:
        raise RequiredArgumentMissingError('Deployment type is mandatory when deploying from URLs. Use --type')


def _validate_ip_address_format(namespace):
    if namespace.ip_address is not None:
        input_value = namespace.ip_address
        if ' ' in input_value:
            raise InvalidArgumentValueError("Spaces not allowed: '{}' ".format(input_value))
        input_ips = input_value.split(',')
        if len(input_ips) > 8:
            raise InvalidArgumentValueError('Maximum 8 IP addresses are allowed per rule.')
        validated_ips = ''
        for ip in input_ips:
            # Use ipaddress library to validate ip network format
            ip_obj = ipaddress.ip_network(ip, False)
            validated_ips += str(ip_obj) + ','
        namespace.ip_address = validated_ips[:-1]


def _validate_ip_address_existence(cmd, namespace):
    resource_group_name = namespace.resource_group_name
    name = namespace.name
    slot = namespace.slot
    scm_site = namespace.scm_site
    configs = _generic_site_operation(cmd.cli_ctx, resource_group_name, name, 'get_configuration', slot)
    access_rules = configs.scm_ip_security_restrictions if scm_site else configs.ip_security_restrictions
    ip_exists = [x.ip_address == namespace.ip_address for x in access_rules]
    if True in ip_exists:
        raise ArgumentUsageError('IP address: ' + namespace.ip_address + ' already exists. '
                                 'Cannot add duplicate IP address values.')


def validate_service_tag(cmd, namespace):
    if namespace.service_tag is not None:
        _validate_service_tag_format(cmd, namespace)
        # For prevention of adding the duplicate IPs.
        if 'add' in cmd.name:
            _validate_service_tag_existence(cmd, namespace)


def _validate_service_tag_format(cmd, namespace):
    if namespace.service_tag is not None:
        input_value = namespace.service_tag
        if ' ' in input_value:
            raise InvalidArgumentValueError("Spaces not allowed: '{}' ".format(input_value))
        input_tags = input_value.split(',')
        if len(input_tags) > 8:
            raise InvalidArgumentValueError('Maximum 8 service tags are allowed per rule.')
        resource_group_name = namespace.resource_group_name
        name = namespace.name
        webapp = _generic_site_operation(cmd.cli_ctx, resource_group_name, name, 'get')
        service_tag_full_list = ListServiceTags(cli_ctx=cmd.cli_ctx)(command_args={
            "location": webapp.location
        })
        if namespace.skip_service_tag_validation is None:
            if service_tag_full_list is None or "values" not in service_tag_full_list:
                logger.warning('Not able to get full Service Tag list. Cannot validate Service Tag.')
                return
            for tag in input_tags:
                valid_tag = False
                for tag_full_list in service_tag_full_list["values"]:
                    if tag.lower() == tag_full_list["name"].lower():
                        valid_tag = True
                        continue
                if not valid_tag:
                    raise InvalidArgumentValueError('Unknown Service Tag: ' + tag)


def _validate_service_tag_existence(cmd, namespace):
    resource_group_name = namespace.resource_group_name
    name = namespace.name
    slot = namespace.slot
    scm_site = namespace.scm_site
    input_tag_value = namespace.service_tag.replace(' ', '')
    configs = _generic_site_operation(cmd.cli_ctx, resource_group_name, name, 'get_configuration', slot)
    access_rules = configs.scm_ip_security_restrictions if scm_site else configs.ip_security_restrictions
    for rule in access_rules:
        if rule.ip_address and rule.ip_address.lower() == input_tag_value.lower():
            raise ArgumentUsageError('Service Tag: ' + namespace.service_tag + ' already exists. '
                                     'Cannot add duplicate Service Tag values.')


def validate_public_cloud(cmd):
    from azure.cli.core.cloud import AZURE_PUBLIC_CLOUD
    if cmd.cli_ctx.cloud.name != AZURE_PUBLIC_CLOUD.name:
        raise ValidationError('This command is not yet supported on soveriegn clouds.')


def validate_staticsite_sku(cmd, namespace):
    from azure.mgmt.web import WebSiteManagementClient
    client = get_mgmt_service_client(cmd.cli_ctx, WebSiteManagementClient).static_sites
    sku_name = client.get_static_site(namespace.resource_group_name, namespace.name).sku.name
    if sku_name.lower() != "standard":
        raise ValidationError("Invalid SKU: '{}'. Staticwebapp must have 'Standard' SKU".format(sku_name))


def validate_staticsite_link_function(cmd, namespace):
    from azure.mgmt.web import WebSiteManagementClient
    validate_staticsite_sku(cmd, namespace)

    if not is_valid_resource_id(namespace.function_resource_id):
        raise ArgumentUsageError("--function-resource-id must specify a function resource ID. "
                                 "To get resource ID, use the following commmand, inserting the function "
                                 "group/name as needed: \n"
                                 "az functionapp show --resource-group \"[FUNCTION_RESOURCE_GROUP]\" "
                                 "--name \"[FUNCTION_NAME]\" --query id ")

    client = get_mgmt_service_client(cmd.cli_ctx, WebSiteManagementClient, api_version="2020-12-01").static_sites
    functions = client.get_user_provided_function_apps_for_static_site(
        name=namespace.name, resource_group_name=namespace.resource_group_name)
    if list(functions):
        raise ValidationError("Cannot have more than one user provided function app associated with a Static Web App")


def validate_functionapp(cmd, namespace):
    validate_vnet_integration(cmd, namespace)
    validate_registry_server(namespace)
    validate_registry_user(namespace)
    validate_registry_pass(namespace)


# TODO consider combining with validate_add_vnet
def validate_vnet_integration(cmd, namespace):
    validate_tags(namespace)
    if _get_environment(namespace):
        if namespace.vnet:
            raise ArgumentUsageError(
                "Invalid input. '--vnet' is not a supported property for function apps deployed to Azure Container "
                "Apps.",
                "Please try again without '--vnet' and configure vnet from Azure Container Apps environment.")
        if namespace.subnet:
            raise ArgumentUsageError(
                "Invalid input. '--subnet' is not a supported property for function apps deployed to Azure Container "
                "Apps.",
                "Please try again without '--subnet' and configure subnet from Azure Container Apps environment.")
    if namespace.subnet or namespace.vnet:
        if not namespace.subnet:
            raise ArgumentUsageError("Cannot use --vnet without --subnet")
        if not is_valid_resource_id(namespace.subnet) and not namespace.vnet:
            raise ArgumentUsageError("Must either specify subnet by resource ID or include --vnet argument")

        client = web_client_factory(cmd.cli_ctx)
        if is_valid_resource_id(namespace.plan):
            parse_result = parse_resource_id(namespace.plan)
            plan_info = client.app_service_plans.get(parse_result['resource_group'], parse_result['name'])
        elif _get_flexconsumption_location(namespace):
            return
        elif _get_consumption_plan_location(namespace):
            raise ArgumentUsageError("Virtual network integration is not allowed for consumption plans.")
        else:
            plan_info = client.app_service_plans.get(name=namespace.plan,
                                                     resource_group_name=namespace.resource_group_name)

        sku_name = plan_info.sku.name
        disallowed_skus = {'FREE', 'SHARED', 'PremiumContainer', 'Isolated', 'IsolatedV2'}
        if get_sku_tier(sku_name) in disallowed_skus:
            raise ArgumentUsageError("App Service Plan has invalid sku for vnet integration: {}."
                                     "Plan sku cannot be one of: {}. "
                                     "Please run 'az appservice plan create -h' "
                                     "to see all available App Service Plan SKUs ".format(sku_name, disallowed_skus))


def _validate_ase_exists(client, ase_name, ase_rg):
    extant_ase = get_resource_if_exists(client.app_service_environments,
                                        resource_group_name=ase_rg, name=ase_name)
    if extant_ase is None:
        raise ValidationError("App Service Environment {} does not exist.".format(ase_name))


# if the ASP exists, validate that it is in the ASE
def _validate_plan_in_ase(client, plan_name, plan_rg, ase_id):
    if plan_name is not None:
        plan_info = get_resource_if_exists(client.app_service_plans,
                                           resource_group_name=plan_rg, name=plan_name)
        if plan_info is not None:
            plan_hosting_env = plan_info.hosting_environment_profile

            if not plan_hosting_env or plan_hosting_env.id != ase_id:
                raise ValidationError("Plan {} already exists and is not in the "
                                      "app service environment.".format(plan_name))


def _validate_ase_is_v3(ase):
    if ase.kind.upper() != "ASEV3":
        raise ValidationError("Only V3 App Service Environments supported")


def _validate_ase_not_ilb(ase):
    if (ase.internal_load_balancing_mode != 0) and (ase.internal_load_balancing_mode != "None"):
        raise ValidationError("Internal Load Balancer (ILB) App Service Environments not supported")


def validate_webapp_up(cmd, namespace):
    if namespace.runtime and namespace.html:
        raise MutuallyExclusiveArgumentError('Conflicting parameters: cannot have both --runtime and --html specified.')

    client = web_client_factory(cmd.cli_ctx)
    if namespace.app_service_environment:
        ase_name, ase_rg, ase_id = get_resource_name_and_group(cmd, namespace.app_service_environment,
                                                               namespace.resource_group_name,
                                                               namespace="Microsoft.Web",
                                                               type="hostingEnvironments")
        _validate_ase_exists(client, ase_name, ase_rg)
        _validate_plan_in_ase(client, namespace.plan, namespace.resource_group_name, ase_id)

        ase = client.app_service_environments.get(resource_group_name=ase_rg, name=ase_name)
        _validate_ase_is_v3(ase)
        _validate_ase_not_ilb(ase)


def _get_app_name(namespace):
    if hasattr(namespace, "name"):
        return namespace.name
    if hasattr(namespace, "webapp"):
        return namespace.webapp
    return None


def _get_environment(namespace):
    if hasattr(namespace, "environment"):
        return namespace.environment
    return None


def _get_flexconsumption_location(namespace):
    if hasattr(namespace, "flexconsumption_location"):
        return namespace.flexconsumption_location
    return None


def _get_consumption_plan_location(namespace):
    if hasattr(namespace, "consumption_plan_location"):
        return namespace.consumption_plan_location
    return None


def validate_app_is_webapp(cmd, namespace):
    client = web_client_factory(cmd.cli_ctx)
    name = _get_app_name(namespace)
    rg = namespace.resource_group
    app = get_resource_if_exists(client.web_apps, name=name, resource_group_name=rg)
    if is_functionapp(app):
        raise ValidationError(f"App '{name}' in group '{rg}' is a function app.")
    if is_logicapp(app):
        raise ValidationError(f"App '{name}' in group '{rg}' is a logic app.")


def validate_app_is_functionapp(cmd, namespace):
    client = web_client_factory(cmd.cli_ctx)
    name = _get_app_name(namespace)
    rg = namespace.resource_group
    app = get_resource_if_exists(client.web_apps, name=name, resource_group_name=rg)
    if is_logicapp(app):
        raise ValidationError(f"App '{name}' in group '{rg}' is a logic app.")
    if is_webapp(app):
        raise ValidationError(f"App '{name}' in group '{rg}' is a web app.")


def validate_centauri_delete_function(cmd, namespace):
    resource_group_name = namespace.resource_group_name
    name = namespace.name
    if is_centauri_functionapp(cmd, resource_group_name, name):
        raise ValidationError(
            "Invalid Operation. This function is currently present in your image",
            "Please modify your image to remove the function and provide an updated image.")


def validate_registry_server(namespace):
    if namespace.environment and namespace.registry_server:
        if not namespace.registry_username or not namespace.registry_password:
            if ACR_IMAGE_SUFFIX not in namespace.registry_server:
                raise RequiredArgumentMissingError("Usage error: --registry-server, --registry-password and"
                                                   " --registry-username are required together if not using Azure Container Registry")  # pylint: disable=line-too-long


def validate_registry_user(namespace):
    if namespace.environment and namespace.registry_username:
        if not namespace.registry_server or (not namespace.registry_password and ACR_IMAGE_SUFFIX not in namespace.registry_server):  # pylint: disable=line-too-long
            raise RequiredArgumentMissingError("Usage error: --registry-server, --registry-password and"
                                               " --registry-username are required together if not using Azure Container Registry")  # pylint: disable=line-too-long


def validate_registry_pass(namespace):
    if namespace.environment and namespace.registry_password:
        if not namespace.registry_server or (not namespace.registry_username and ACR_IMAGE_SUFFIX not in namespace.registry_server):  # pylint: disable=line-too-long
            raise RequiredArgumentMissingError("Usage error: --registry-server, --registry-password and"
                                               " --registry-username are required together if not using Azure Container Registry")  # pylint: disable=line-too-long
