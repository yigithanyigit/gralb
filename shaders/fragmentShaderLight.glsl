#version 330 core

struct Light {
    int type;
    vec3 position;
    vec3 direction;
    vec3 color;
    float cutoff;

    float constant;
    float linear;
    float quadratic;

    bool enabled;
};


struct Material {
    float shininess;
};

uniform bool blinnPhong = true;

uniform Light pointLight;
uniform Light directionalLight;
uniform Light spotLight;

uniform sampler2D tex1;

uniform Material material;

uniform mat4 view;

in vec3 fragPosition;
in vec4 fragColor;
in vec2 fragUV;
in vec3 fragNormal;
in vec3 fragViewDir;

out vec4 outColor;

void calculateBlinnPhong(inout vec3 result ,vec3 viewDir, vec3 normal, vec3 lightDir)
{
    //https://stackoverflow.com/questions/20008089/specular-lighting-appears-on-both-eye-facing-and-rear-sides-of-object
    if(dot(viewDir, normal) > 0)
    {
        vec3 reflectDir = reflect(-lightDir, normal);

        float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
        vec3 specular = 1 * spec * directionalLight.color;

        result += specular;
    }
}

void CalculatePointLight(inout vec3 result, vec3 viewDir, vec3 normal)
{
    vec3 lightDir = normalize(pointLight.position - fragPosition);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * pointLight.color;

    if(blinnPhong == true)
        calculateBlinnPhong(result, viewDir, normal, lightDir);

    result += diffuse;

}

void CalculateSpotLight(inout vec3 result, vec3 viewDir, vec3 normal)
{
    vec3 lightDir = normalize(spotLight.position - fragPosition);

    float spotFactor = dot(normalize(spotLight.direction), -lightDir);

    if (spotFactor > cos(radians(spotLight.cutoff))) {

        float diff = max(dot(normal, lightDir), 0.0);
        vec3 diffuse = diff * pointLight.color;

        if(blinnPhong == true)
            calculateBlinnPhong(result, viewDir, normal, lightDir);

        result += diffuse;

    }
}

void CalculateDirectionalLight(inout vec3 result, vec3 viewDir, vec3 normal)
{
    vec3 lightDir = normalize(-directionalLight.direction);
    float diff = max(dot(normal, lightDir), 0.0);
    vec3 diffuse = diff * directionalLight.color;

    if(blinnPhong == true)
        calculateBlinnPhong(result, viewDir, normal, lightDir);

    result += diffuse;
}




void main() {
    // Ambient light
    vec3 ambient = vec3(0.1, 0.1, 0.1);

    vec3 result = vec3(0.0);

    vec4 texVal = texture(tex1, fragUV);

    vec3 normal = normalize(fragNormal);

    vec3 viewDir = normalize(vec3(view[3]) - fragPosition);

    vec3 lightDir = normalize(pointLight.position - fragPosition);

    if(pointLight.enabled == true)
    {
        CalculatePointLight(result, viewDir, normal);
    }
    if(directionalLight.enabled == true)
    {
        CalculateDirectionalLight(result, viewDir, normal);
    }
    if(spotLight.enabled == true)
    {
        CalculateSpotLight(result, viewDir, normal);
    }

    // Combine ambient and accumulated diffuse/specular light
    result += (ambient);
    //result = vec3(view) + ambient;

    outColor = vec4(result * texVal.rgb, texVal.a);
}
