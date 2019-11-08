package info.novatec.bpm.camunda_test_spring_boot;

import static org.camunda.bpm.engine.test.assertions.bpmn.AbstractAssertions.init;
import static org.camunda.bpm.engine.test.assertions.bpmn.BpmnAwareAssertions.assertThat;
import static org.camunda.bpm.engine.test.assertions.bpmn.BpmnAwareTests.complete;
import static org.camunda.bpm.engine.test.assertions.bpmn.BpmnAwareTests.task;
import static org.camunda.bpm.engine.test.assertions.bpmn.BpmnAwareTests.withVariables;

import javax.annotation.PostConstruct;

import org.camunda.bpm.engine.ProcessEngine;
import org.camunda.bpm.engine.RuntimeService;
import org.camunda.bpm.engine.runtime.ProcessInstance;
import org.camunda.bpm.engine.test.Deployment;
import org.camunda.bpm.engine.test.ProcessEngineRule;
import org.camunda.bpm.extension.process_test_coverage.junit.rules.TestCoverageProcessEngineRuleBuilder;
import org.junit.Before;
import org.junit.ClassRule;
import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.context.SpringBootTest.WebEnvironment;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;

import info.novatec.bpm.camunda_test_spring_boot.delegates.SomethingDoer;
import info.novatec.bpm.camunda_test_spring_boot.delegates.SomethingElseDoer;

/**
 * Test case starting an in-memory database-backed Process Engine.
 */
@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = WebEnvironment.NONE)
public class ProcessTest {

    private static final String PROCESS_DEFINITION_KEY = "camunda-test-spring-boot";

    @Autowired
    private ProcessEngine processEngine;

    @MockBean
    private SomethingElseDoer somethingElseDoer;

    @MockBean
    private SomethingDoer somethingDoer;

    RuntimeService runtimeService;

    @Rule
    @ClassRule
    public static ProcessEngineRule rule;

    @PostConstruct
    void initRule() {
        rule = TestCoverageProcessEngineRuleBuilder.create(processEngine).build();
    }

    @Before
    public void setup() {
        init(processEngine);
        this.runtimeService = rule.getRuntimeService();
    }

    @Test
    @Deployment(resources = "process.bpmn")
    public void testHappyPath() {
        ProcessInstance processInstance = runtimeService.startProcessInstanceByKey(PROCESS_DEFINITION_KEY);
        assertThat(processInstance).isActive();

        assertThat(processInstance).isWaitingAtExactly("userTask1");
        complete(task(), withVariables("input", 1));

        assertThat(processInstance).isEnded();
    }

    @Test
    @Deployment(resources = "process.bpmn")
    public void testUnHappyPath() {
        ProcessInstance processInstance = runtimeService.startProcessInstanceByKey(PROCESS_DEFINITION_KEY);
        assertThat(processInstance).isActive();

        assertThat(processInstance).isWaitingAtExactly("userTask1");
        complete(task(), withVariables("input", 2));

        assertThat(processInstance).isEnded();
    }

}
