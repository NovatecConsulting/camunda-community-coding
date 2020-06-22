package camunda;

import org.camunda.bpm.engine.AuthorizationService;
import org.camunda.bpm.engine.FilterService;
import org.camunda.bpm.engine.IdentityService;
import org.camunda.bpm.engine.TaskService;
import org.camunda.bpm.engine.authorization.Authorization;
import org.camunda.bpm.engine.authorization.Resources;
import org.camunda.bpm.engine.filter.Filter;
import org.camunda.bpm.engine.identity.Group;
import org.camunda.bpm.engine.identity.User;
import org.camunda.bpm.engine.task.TaskQuery;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.SmartLifecycle;
import org.springframework.stereotype.Component;

import java.lang.invoke.MethodHandles;
import java.util.ArrayList;

/**
 * The component creates all default users, groups and filters
 * inspired by  * https://github.com/Educama/Showcase/blob/master/backend/src/main/java/org/educama/application/lifecycle/DefaultUserLifecycleBean.java
 */
@Component
public class DefaultUsers implements SmartLifecycle {
    @Autowired
    IdentityService identityService;

    @Autowired
    AuthorizationService authorizationService;

    @Autowired
    TaskService taskService;

    @Autowired
    FilterService filterService;

    private final Logger logger = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());
    private boolean running;

    @Override
    public boolean isAutoStartup() {
        return true;
    }

    @Override
    public void stop(Runnable runnable) {
        running = false;
        runnable.run();
    }

    @Override
    public void start() {

        logger.info("Creating default users and filters");
        User adminUser = createUser("admin", "admin", "admin", "admin");
        ArrayList<User> admins = new ArrayList<User>();
        admins.add(adminUser);
        Group adminGroup = createGroup("camunda-admin", "camunda-admin", admins);

        User julianUser = createUser("julian", "demo", "Julian", "Müller");
        User felixUser = createUser("felix", "demo", "Felix", "Schmidt");
        User annaUser = createUser("anna", "demo", "Anna", "Schneider");

        ArrayList<User> service = new ArrayList<User>();
        service.add(felixUser);
        service.add(annaUser);
        service.add(adminUser);
        Group serviceGroup = createGroup("service", "WORKFLOW", service);

        ArrayList<User> kitchen = new ArrayList<User>();
        kitchen.add(julianUser);
        kitchen.add(adminUser);
        Group kitchenGroup = createGroup("kitchen", "WORKFLOW", kitchen);

        grantAuthorizationWithPermissions(adminGroup);
        createFilters();
        logger.info("All users and filters created");
    }

    @Override
    public void stop() {
        running = false;
    }

    @Override
    public boolean isRunning() {
        return running;
    }

    @Override
    public int getPhase() {
        return 1;
    }

    private User createUser(String username, String password, String firstName, String lastName) {
        User user = identityService.newUser(username);
        user.setPassword(password);
        user.setFirstName(firstName);
        user.setLastName(lastName);
        identityService.saveUser(user);

        return user;
    }

    private Group createGroup(String name, String type, ArrayList<User> users) {
        Group group = identityService.newGroup(name);
        group.setName(name);
        group.setType(type);
        identityService.saveGroup(group);
        users.forEach((it) -> identityService.createMembership(it.getId(), group.getId()));

        return group;
    }

    private void grantAuthorizationWithPermissions(Group adminGroup) {
        Authorization authorization = authorizationService.createNewAuthorization(Authorization.AUTH_TYPE_GRANT);
        authorization.setGroupId(adminGroup.getId());
        authorization.setResource(Resources.USER);
        authorization.addPermission(org.camunda.bpm.engine.authorization.Permissions.ALL);
        authorizationService.saveAuthorization(authorization);
    }

    private void createFilters() {
        TaskQuery query = taskService.createTaskQuery();
        Filter allTasksFilter = filterService.newTaskFilter().setName("All Tasks").setOwner("admin").setQuery(query);
        filterService.saveFilter(allTasksFilter);

        query = taskService.createTaskQuery().taskCandidateGroup("service").includeAssignedTasks();
        Filter serviceTasksFilter = filterService.newTaskFilter().setName("Service").setOwner("admin").setQuery(query);
        filterService.saveFilter(serviceTasksFilter);

        query = taskService.createTaskQuery().taskCandidateGroup("kitchen").includeAssignedTasks();
        Filter kitchenTasksFilter = filterService.newTaskFilter().setName("Kitchen").setOwner("admin").setQuery(query);
        filterService.saveFilter(kitchenTasksFilter);
    }
}
