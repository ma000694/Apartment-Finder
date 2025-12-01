package com.umnapartmentfinder.listings;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InfoController {
    
    @GetMapping("/apartment")
    public String search(@RequestParam String apartment){
        String file = "src//main//apartmentInfo.csv";
        BufferedReader reader = null;
        String line = "";
        List<String> infoList = new ArrayList<>();
        try {
            reader = new BufferedReader(new FileReader(file));
            while(null != (line = reader.readLine())) {
                String[] row = line.split(",");
                if (line.contains(apartment)) {
                    infoList.add("Price: "+ row[4] + ", " + row[5]);
                }
            }
        }
        catch(Exception e) {
            e.printStackTrace();
        }
        finally {
            try {
                reader.close();
            }
            catch (IOException e){
                e.printStackTrace();
            }
        }

        return "Available floor plans at '" + apartment + "':\n\n" + infoList;


    }
}
