#version 330

in vec4 fragColor;
in vec2 fragUV;
in vec3 fragNormal;
in vec3 fragViewDir;

out vec4 outColor;

uniform vec3 lightDir;
uniform vec4 lightColor;
uniform float lightIntensity;

uniform sampler2D tex1;

uniform float shininess = 35.0;


void main()
{

    //outColor = vec4(fragNormal, 1.0);

	vec4 texVal = texture(tex1, fragUV);

    // Lambertian diffuse shading model
    float nDotL = max(dot(fragNormal, lightDir), 0.0);
    vec3 diffuse = texVal.rgb * lightColor.rgb * lightIntensity * nDotL;

    // Blinn-Phong specular reflection model
    vec3 halfwayDir = normalize(lightDir + fragViewDir);
    float spec = pow(max(dot(fragNormal, halfwayDir), 0.0), shininess);
    vec3 specular = lightColor.rgb * spec;

    // Combine ambient, diffuse, and specular components
    vec3 ambient = 0.02 * fragColor.rgb;
    vec3 resultColor = ambient + diffuse + specular;

    // Combine the diffuse color with the texture value
    outColor = vec4(resultColor, texVal.a);
    // outColor = texVal;


}
