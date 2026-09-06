# Criticality Calculation

The calculator uses a one-speed neutron model with the assumption of zero neutron leakage.

For species $i$, the macroscopic absorption cross section is:

$$\Sigma_{a,i} = N_i \sigma_{a,i}$$

where:

- $N_i$ is the number density in $\text{m}^{-3}$
- $\sigma_{a,i}$ is the microscopic absorption cross section

The neutron-production contribution is:

$$\nu\Sigma_{f,i} = \nu_i N_i \sigma_{f,i}$$

where:

- $\nu_i$ is the average number of neutrons produced per fission
- $\sigma_{f,i}$ is the microscopic fission cross section

The total macroscopic absorption cross section is obtained by summing the contributions from all species:

$$\Sigma_a = \sum_i \Sigma_{a,i} = \sum_i N_i \sigma_{a,i}$$

Similarly, the total neutron-production cross section is:

$$\nu\Sigma_f = \sum_i \nu\Sigma_{f,i} = \sum_i \nu_i N_i \sigma_{f,i}$$

Under the zero-leakage assumption, the neutron multiplication factor is the ratio of neutron production to neutron absorption:

$$k = \frac{\nu\Sigma_f}{\Sigma_a}$$

Substituting the expressions for the total neutron-production and absorption cross sections gives:

$$k = \frac{\sum_i \nu_i N_i \sigma_{f,i}}{\sum_i N_i \sigma_{a,i}}$$

The criticality state is classified according to the calculated multiplication factor:

- **Subcritical:** $k < 1$
- **Critical:** $k \approx 1$
- **Supercritical:** $k > 1$

The implementation uses a numerical tolerance when determining whether the multiplication factor is approximately equal to one.

# Cross-Section Units

Microscopic cross sections are provided in barns, where:

$$1\text{ barn} = 10^{-28}\text{ m}^2$$

The cross sections are converted to square metres before calculating the macroscopic cross sections.

Since number density has units of $\text{m}^{-3}$ and microscopic cross section has units of $\text{m}^2$:

$$[\Sigma] = \text{m}^{-3}\text{m}^2 = \text{m}^{-1}$$

Therefore, both $\Sigma_a$ and $\nu\Sigma_f$ have units of $\text{m}^{-1}$, while their ratio $k$ is dimensionless.

# Model Assumptions

The calculation assumes:

- One-speed neutron behaviour
- Thermal neutron cross-section data
- Zero neutron leakage
- Homogeneous material composition
- Constant microscopic cross sections
- User-specified number density for each species

The zero-leakage assumption means that neutron losses from the physical boundaries of a finite reactor are not represented. The calculated multiplication factor therefore describes the simplified model implemented by the application rather than a full finite-reactor criticality calculation.