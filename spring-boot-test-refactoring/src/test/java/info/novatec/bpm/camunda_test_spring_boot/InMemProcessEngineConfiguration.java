package info.novatec.bpm.camunda_test_spring_boot;

import javax.sql.DataSource;

import org.camunda.bpm.engine.ProcessEngineConfiguration;
import org.camunda.bpm.engine.impl.cfg.ProcessEngineConfigurationImpl;
import org.camunda.bpm.engine.impl.el.ExpressionManager;
import org.camunda.bpm.engine.spring.ProcessEngineFactoryBean;
import org.camunda.bpm.engine.spring.SpringExpressionManager;
import org.camunda.bpm.extension.process_test_coverage.spring.SpringProcessWithCoverageEngineConfiguration;
import org.h2.Driver;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.jdbc.datasource.DataSourceTransactionManager;
import org.springframework.jdbc.datasource.SimpleDriverDataSource;
import org.springframework.transaction.PlatformTransactionManager;

public class InMemProcessEngineConfiguration {

    @Autowired
    ApplicationContext applicationContext;

    @Bean
    public javax.sql.DataSource dataSource() {
        SimpleDriverDataSource datasource = new SimpleDriverDataSource();

        datasource.setDriverClass(Driver.class);
        datasource.setUrl("jdbc:h2:mem:camunda-test;DB_CLOSE_ON_EXIT=false;DB_CLOSE_DELAY=-1");
        datasource.setUsername("sa");
        datasource.setPassword("");

        return datasource;
    }

    @Bean
    public PlatformTransactionManager transactionManager(@Autowired DataSource datasource) {
        return new DataSourceTransactionManager(datasource);
    }

    @Bean
    public ProcessEngineConfigurationImpl processEngineConfiguration(@Autowired DataSource datasource,
        @Autowired PlatformTransactionManager transactionManager, @Autowired ExpressionManager expressionManager) {
        SpringProcessWithCoverageEngineConfiguration config = new SpringProcessWithCoverageEngineConfiguration();

        config.setExpressionManager(expressionManager);
        config.setTransactionManager(transactionManager);
        config.setDataSource(datasource);

        config.setHistory(ProcessEngineConfiguration.HISTORY_FULL);
        config.setJobExecutorActivate(false);
        config.setDatabaseSchemaUpdate("true");

        config.init();
        return config;
    }

    @Bean
    public ExpressionManager expressionManager() {
        return new SpringExpressionManager(applicationContext, null);
    }

    @Bean
    public ProcessEngineFactoryBean processEngine(
        @Autowired ProcessEngineConfigurationImpl processEngineConfiguration) {
        ProcessEngineFactoryBean processEngineFactoryBean = new ProcessEngineFactoryBean();
        processEngineFactoryBean.setProcessEngineConfiguration(processEngineConfiguration);

        return processEngineFactoryBean;
    }
}
