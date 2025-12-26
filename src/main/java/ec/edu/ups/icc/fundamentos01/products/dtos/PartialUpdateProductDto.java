package ec.edu.ups.icc.fundamentos01.products.dtos;

import jakarta.validation.constraints.Positive;
import jakarta.validation.constraints.Size;

public class PartialUpdateProductDto {

    @Size(min = 3, max = 150)
    public String name;

    @Positive
    public Double price;

    @Size(max = 500)
    public String description;
}
