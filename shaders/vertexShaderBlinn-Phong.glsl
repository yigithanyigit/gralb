#version 330

layout(location = 0) in vec4 vertexPosition;
layout(location = 1) in vec4 vertexColor;
layout(location = 2) in vec2 vertexUV;
layout(location = 3) in vec4 vertexNormal;

out vec4 fragColor;
out vec2 fragUV;
out vec3 fragNormal;
out vec3 fragViewDir;
out vec3 fragPosition;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

void main()
{
	vec4 worldPos = proj * view * model * vertexPosition;
	fragColor = vertexColor;
	fragUV = vertexUV;
	fragNormal = vec3(transpose(inverse(model)) * vertexNormal);
	fragViewDir = vec3(transpose(inverse(view * model)) * vec4(fragNormal, 1.0));
	fragPosition = vec3(model * vec4(vertexPosition.xyz, 1.0));
	gl_Position = worldPos;

}