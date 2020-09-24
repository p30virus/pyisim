from attr import attributes
from isimws.exceptions import *
from isimws.entities import (
    Activity,
    Access,
    OrganizationalContainer,
    Person,
    Service,
    StaticRole,
    ProvisioningPolicy,
    Group,
)


def groups(sesion, by, service_dn=None, group_profile_name="", group_info=""):
    """Buscar grupos.

    Args:
        by (string): "account", "access" or "service"
        dn (string): account or access dn
        groupProfileName (string, optional): Group profile name if searching by service. Defaults to None.
        groupInfo (string, optional): Group name or description if searching by service. Defaults to None.

    Raises:
        NotImplementedError: Search by account or access not implemented yet.
        InvalidOptionError

    Returns:
        list: Search results
    """
    sesion = sesion.soapclient
    if by == "account":
        raise NotImplementedError
    elif by == "access":
        raise NotImplementedError
    elif by == "service":
        ret = sesion.buscarGruposPorServicio(service_dn, group_profile_name, group_info)
    else:
        raise InvalidOptionError("Invalid option")

    return [Group(sesion, group=g) for g in ret]


def people(
    sesion,
    filter="*",
    by="cn",
    profile_name="Person",
    attributes="*",
    embedded="",
    limit=50,
):
    """ "Wrapper para buscar/lookup personas o bpperson desde REST API

    Args:
        sesion ([isimws.auth.Session]): Sesión de isimws
        profile (str): Person/BPPerson
        by (str, optional): Atributo por el que buscar. Defaults to "cn".
        filter (str, optional): Filtro por el que buscar. Defaults to "*".
        attributes (str, optional): Atributos a retornar. Defaults to "dn".
        embedded (str, optional): Atributos embebidos a retornar (ej. manager.cn). Defaults to "".
        limit (int, optional): Defaults to 50.

    Returns:
        [list(Person)]: listado de personas encontradas
    """

    ret = sesion.restclient.buscarPersonas(
        profile_name,
        atributos=attributes,
        embedded=embedded,
        buscar_por=by,
        filtro=filter,
        limit=limit,
    )
    personas = [Person(sesion, person=p) for p in ret]
    return personas


def provisioning_policy(sesion, name, parent: OrganizationalContainer):

    wsou = parent.wsou
    results = sesion.soapclient.buscarPoliticaSuministro(
        wsou, nombre_politica=name, find_unique=False
    )
    return [ProvisioningPolicy(sesion, provisioning_policy=p) for p in results]


def roles(sesion, by="errolename", filter="*", find_unique=False):
    soap = sesion.soapclient
    results = soap.buscarRol(f"({by}={filter})", find_unique)
    return [StaticRole(sesion, rol=r) for r in results]


def activities(sesion, by="activityName", filter="*"):
    """Busca actividades

    Args:
        sesion (isimws.auth.Session): Sesión de isimws
        by (str, optional): Filtros disponibles por ISIM REST API (activityId, nombres de actividad/servicio/participantes) o requestId. Defaults to "activityName".
        filter (str, optional): Filtro. Defaults to "*".
    """

    if by == "requestId":
        # sesion.soapclient.buscarActividadesDeSolicitud(filter)
        """ RESPUESTA IBM A getRecurseSubProcess()
        Your observation is correct. The backend code returns the activities belonging to the first level sub-process only. 
        I feel the main confusion is due to the lack of documentation around this API and the name of the parameter used. 
        The intent of introducing this additional boolean flag was to restrict the result to only the direct activities of the main process. 
        It should have been “getImmediateChildActivities” rather than “recurseSubProcesses”.
        The customer can accomplish this by using a combination of getActivities() and getChildProcesses().
        """
        results = sesion.restclient.buscarActividad(
            solicitudID=f"/itim/rest/requests/{filter}"
        )
    else:
        results = sesion.restclient.buscarActividad(
            search_attr=by, search_filter=filter
        )

    return [Activity(sesion, activity=a) for a in results]


def access(sesion, by="accessName", filter="*", attributes="", limit=20):

    ret = sesion.restclient.buscarAcceso(
        by=by, filtro=filter, atributos=attributes, limit=limit
    )
    accesos = [Access(access=a) for a in ret]

    return accesos


def service(sesion, parent: OrganizationalContainer, by="erservicename", filter="*"):

    # ret=sesion.restclient.buscarServicio(by,filter,limit,atributos=attributes)
    # servicios=[Service(sesion,service=s) for s in ret]
    ret = sesion.soapclient.buscarServicio(
        parent.wsou, f"({by}={filter})", find_unique=False
    )
    servicios = [Service(sesion, service=s) for s in ret]

    return servicios


def organizational_container(sesion, profile_name, filter, by="name"):
    """[summary]

    Args:
        sesion (isimws.Session)
        profile_name (str): ["bporganizations", "organizationunits", "organizations","locations","admindomains"]
        filter (str): name or attr value
        by (str, optional): attribute to search by. Defaults to "name".

    Returns:
        isimws.entities.OrganizationalContainer
    """

    buscar_por = None if by == "name" else by
    ret = sesion.restclient.buscarOUs(
        profile_name, buscar_por=buscar_por, filtro=filter, attributes="dn"
    )

    ous = [OrganizationalContainer(sesion, organizational_container=ou) for ou in ret]

    return ous
