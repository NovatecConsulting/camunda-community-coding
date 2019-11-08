package info.novatec.bpm.camunda_test_spring_boot;

import static org.camunda.bpm.engine.test.assertions.bpmn.BpmnAwareAssertions.assertThat;
import static org.camunda.bpm.engine.test.assertions.bpmn.BpmnAwareTests.complete;
import static org.camunda.bpm.engine.test.assertions.bpmn.BpmnAwareTests.task;
import static org.camunda.bpm.engine.test.assertions.bpmn.BpmnAwareTests.withVariables;

import org.camunda.bpm.engine.RuntimeService;
import org.camunda.bpm.engine.runtime.ProcessInstance;
import org.camunda.bpm.engine.test.Deployment;
import org.camunda.bpm.engine.test.ProcessEngineRule;
import org.camunda.bpm.extension.mockito.DelegateExpressions;
import org.camunda.bpm.extension.process_test_coverage.junit.rules.TestCoverageProcessEngineRuleBuilder;
import org.junit.Before;
import org.junit.ClassRule;
import org.junit.Rule;
import org.junit.Test;

public class ProcessTest {

    private static final String PROCESS_DEFINITION_KEY = "camunda-test-spring-boot";

    @Rule
    @ClassRule
    public static ProcessEngineRule rule = TestCoverageProcessEngineRuleBuilder.create().build();

    RuntimeService runtimeService;

    @Before
    public void setup() {
        runtimeService = ProcessTest.rule.getRuntimeService();

        DelegateExpressions.registerJavaDelegateMock("somethingDoer");
        DelegateExpressions.registerJavaDelegateMock("somethingElseDoer");
        DelegateExpressions.registerExecutionListenerMock("myListener");
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
