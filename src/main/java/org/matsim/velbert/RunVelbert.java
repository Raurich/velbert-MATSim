package org.matsim.velbert;

import org.matsim.api.core.v01.TransportMode;
import org.matsim.core.config.ConfigUtils;
import org.matsim.core.config.groups.PlanCalcScoreConfigGroup;
import org.matsim.core.config.groups.PlansCalcRouteConfigGroup;
import org.matsim.core.controler.AbstractModule;
import org.matsim.core.controler.Controler;
import org.matsim.core.scenario.ScenarioUtils;

import java.util.Arrays;
import java.util.List;

public class RunVelbert {

    public static void main(String[] args) {

        final String PT_CONST = args[0];
        final String BIKE_CONST = args[1];
        final String CAR_CONST = args[2];

        String[] newArgs = Arrays.copyOfRange(args, 3, args.length);

        var config = ConfigUtils.loadConfig(newArgs);

        config.plansCalcRoute().setAccessEgressType(PlansCalcRouteConfigGroup.AccessEgressType.accessEgressModeToLink);

        config.planCalcScore().addModeParams(new PlanCalcScoreConfigGroup.ModeParams("pt").setConstant(Integer.parseInt(PT_CONST)));
        config.planCalcScore().addModeParams(new PlanCalcScoreConfigGroup.ModeParams("bike").setConstant(Integer.parseInt(BIKE_CONST)));
        config.planCalcScore().addModeParams(new PlanCalcScoreConfigGroup.ModeParams("car").setConstant(Integer.parseInt(CAR_CONST)));
        config.planCalcScore().addModeParams(new PlanCalcScoreConfigGroup.ModeParams("ride").setConstant(Integer.parseInt(CAR_CONST)));

        for (long ii = 600; ii <= 97200; ii += 600) {

            for (String act : List.of("educ_higher", "educ_kiga", "educ_other", "educ_primary", "educ_secondary",
                    "educ_tertiary", "errands", "home", "visit")) {
                config.planCalcScore()
                        .addActivityParams(new PlanCalcScoreConfigGroup.ActivityParams(act + "_" + ii + ".0").setTypicalDuration(ii));
            }

            config.planCalcScore().addActivityParams(new PlanCalcScoreConfigGroup.ActivityParams("work_" + ii + ".0").setTypicalDuration(ii)
                    .setOpeningTime(6. * 3600.).setClosingTime(20. * 3600.));
            config.planCalcScore().addActivityParams(new PlanCalcScoreConfigGroup.ActivityParams("business_" + ii + ".0").setTypicalDuration(ii)
                    .setOpeningTime(6. * 3600.).setClosingTime(20. * 3600.));
            config.planCalcScore().addActivityParams(new PlanCalcScoreConfigGroup.ActivityParams("leisure_" + ii + ".0").setTypicalDuration(ii)
                    .setOpeningTime(9. * 3600.).setClosingTime(27. * 3600.));
            config.planCalcScore().addActivityParams(new PlanCalcScoreConfigGroup.ActivityParams("shop_daily_" + ii + ".0").setTypicalDuration(ii)
                    .setOpeningTime(8. * 3600.).setClosingTime(20. * 3600.));
            config.planCalcScore().addActivityParams(new PlanCalcScoreConfigGroup.ActivityParams("shop_other_" + ii + ".0").setTypicalDuration(ii)
                    .setOpeningTime(8. * 3600.).setClosingTime(20. * 3600.));
        }

        var scenario = ScenarioUtils.loadScenario(config);

        var controler = new Controler(scenario);

        // use the (congested) car travel time for the teleported ride mode
        controler.addOverridingModule(new AbstractModule() {
            @Override
            public void install() {
                addTravelTimeBinding(TransportMode.ride).to(networkTravelTime());
                addTravelDisutilityFactoryBinding(TransportMode.ride).to(carTravelDisutilityFactoryKey());
            }
        });

        controler.run();
    }
}
