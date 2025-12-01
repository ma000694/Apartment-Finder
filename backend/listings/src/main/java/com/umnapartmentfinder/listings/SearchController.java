package com.umnapartmentfinder.listings;

import java.io.*;
import java.util.*;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SearchController {
    
    
    @GetMapping("/search")
    public String search(@RequestParam String term){
        String file = "src//main//apartmentInfo.csv";
        BufferedReader reader = null;
        String line = "";
        List<String> outputList = new ArrayList<>();
        try {
            reader = new BufferedReader(new FileReader(file));
            while((line = reader.readLine()) != null) {
                String[] row = line.split(",");
                if (line.contains(term)) {
                    outputList.add(row[1]);
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


        return "Your search for '" + term + "' has loaded:\n\n" + outputList;
    }
    
}
