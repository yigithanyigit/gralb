/*
#version 330

in vec4 fragColor;
in vec2 fragUV;
in vec3 fragNormal;

out vec4 outColor;

uniform vec3 lightDir;
uniform vec4 lightColor;
uniform float lightIntensity;

uniform sampler2D tex1;

void main()
{

    //outColor = vec4(fragNormal, 1.0);

	vec4 texVal = texture(tex1, fragUV);

    // Lambertian diffuse shading model
    float nDotL = max(dot(fragNormal, lightDir), 0.0);
    vec3 diffuse = texVal.rgb * lightColor.rgb * lightIntensity * nDotL;

    // Combine the diffuse color with the texture value
    outColor = vec4(diffuse, texVal.a);
    // outColor = texVal;


}
